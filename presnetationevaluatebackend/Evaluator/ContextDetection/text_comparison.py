import openai
import boto3
import os
import config
# Initialize OpenAI API client
from Evaluator.ContextDetection.store_to_awsdynamoDB import store_to_awsdynamoDB
from openai import OpenAI

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=config.OPENAI_API_KEY,
)
# Initialize DynamoDB client
# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table('YourDynamoDBTableName')

context_message = {
    "role": "system",
    "content": """
    You are the strict presentation evaluator. For the evaluation you will get 2 text namely, slide-text and audio-text. 
    Slide-text is the text extracted from the slides using OCR so it will be a little jumbled and not clear sometimes. 
    You have to make assumptions to understand the text in slides. Audio-text is words spoken by the presenter so you 
    have to understand text spoken and keeping both in mind you have to evaluate the following parameters and give a 
    score from 0 to 100 in each aspect of the evaluation.
    
    content_coverage: To evaluate content coverage, focus on the completeness aspect by comparing the major points 
    highlighted in the PowerPoint presentation with the spoken content. Check if all key topics and subtopics in the 
    slides are adequately covered in the verbal delivery. Ensure that no significant points are omitted or superficially 
    addressed. This comparison helps determine if the presenter successfully conveys the intended information comprehensively.
    
    correctness: To evaluate correctness, verify that the spoken text accurately reflects the content of the slides. 
    Check if the presenter’s verbal explanations align with the information, data, and points displayed on the slides. 
    Ensure that there are no discrepancies or contradictions between what is said and what is shown. This assessment helps 
    confirm that the presentation maintains consistency and reliability throughout.
    
    consistency_in_words: To evaluate consistency in words, verify that the same terminology and key phrases from the 
    PowerPoint presentation are used in the spoken content. Ensure that the presenter consistently uses the same terms 
    and phrases as those on the slides to avoid confusion and maintain clarity. Check for any variations or substitutions 
    that might alter the intended meaning. This consistency helps reinforce key concepts and ensures the audience understands 
    the message accurately.
    
    textual_cohesion: To evaluate textual cohesion, assess if the spoken content maintains a logical flow that is consistent 
    with the structure of the slides. Ensure that the presentation follows the same sequence and organization as the slides, 
    smoothly transitioning from one point to the next. Verify that the connections between different sections of the spoken 
    content mirror the logical progression on the slides. This alignment helps the audience follow the presentation easily 
    and enhances overall comprehension.
    
    language_and_grammar: To evaluate language and grammar, compare if the language and grammar used in the spoken content 
    is correct and mirrors the quality of the PPT text. Ensure that the spoken content is free of grammatical errors and uses 
    professional, not casual, language. Check that the vocabulary and tone of the spoken content match the formal style of the 
    presentation slides. This consistency maintains the professional standard of the presentation and enhances its credibility.
    
    From now on the input would be:
    slide_text: //text in slide
    audio_text: //text spoken by the speaker
    output given by you should only be a list containing the score of each parameter from 0 to 100 like [content_coverage, 
    correctness, consistency_in_words, textual_cohesion, language_and_grammar] show only the numbers. and follow the following rules
    Rules:
    1) Compare the audio-text to slide-text how well does it satisfy the given parameter.
    2) Content Coverege only give the score if the audio text covers the text in the slide. If not taling about slide-text then give 0.
    3) For Correctness check with knowledge available to you and evaluate strictly. If speaking opposite to the fact then give 0.
    4) Check Consistancy in words by checking if the audio-text has the words appropriate to the slide-text or not.
    5) Check strictly textual_cohension by considering the flow of the sentence whether the sentence in the audio-text is making sense as per the sequence of the statement.
    6) Check the grammer and the language mistake in the audio-text.
    7) If audio-text is empty then all scores are zero.
    """
}

def evaluate_presentation(slide_text, audio_text):
    print("there you go")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[context_message,{"role": "user",  "content":f"You are the presentation evaluator. For the evaluation you will get 2 text namely, slide-text and audio-text. Slide-text is the text extracted from the slides using ocr so it will be little jumbled and not clear sometime you have to make assumption to understand the text in slides. Audio-text is words spoken by the presentor so you have to understand text spoken and keeping both in mind you have to evaluate the following parameters and give a score from 0 to 100 in each aspect of the evaluation.\n\nslide_text: {slide_text}\naudio_text: {audio_text}\n\ncontent_coverage: To evaluate content coverage, focus on the completeness aspect by comparing the major points highlighted in the PowerPoint presentation with the spoken content. Check if all key topics and subtopics in the slides are adequately covered in the verbal delivery. Ensure that no significant points are omitted or superficially addressed. This comparison helps determine if the presenter successfully conveys the intended information comprehensively.\n\ncorrectness: To evaluate correctness, verify that the spoken text accurately reflects the content of the slides. Check if the presenter’s verbal explanations align with the information, data, and points displayed on the slides. Ensure that there are no discrepancies or contradictions between what is said and what is shown. This assessment helps confirm that the presentation maintains consistency and reliability throughout.\n\nconsistency_in_words: To evaluate consistency in words, verify that the same terminology and key phrases from the PowerPoint presentation are used in the spoken content. Ensure that the presenter consistently uses the same terms and phrases as those on the slides to avoid confusion and maintain clarity. Check for any variations or substitutions that might alter the intended meaning. This consistency helps reinforce key concepts and ensures the audience understands the message accurately.\n\nt textual_cohension: To evaluate textual cohesion, assess if the spoken content maintains a logical flow that is consistent with the structure of the slides. Ensure that the presentation follows the same sequence and organization as the slides, smoothly transitioning from one point to the next. Verify that the connections between different sections of the spoken content mirror the logical progression on the slides. This alignment helps the audience follow the presentation easily and enhances overall comprehension.\n\nlanguage_and_grammar: To evaluate language and grammar, compare if the language and grammar used in the spoken content is correct and mirrors the quality of the PPT text. Ensure that the spoken content is free of grammatical errors and uses professional, not casual, language. Check that the vocabulary and tone of the spoken content match the formal style of the presentation slides. This consistency maintains the professional standard of the presentation and enhances its credibility.\n\nOutput: [content_coverage, correctness, consistency_in_words, textual_cohension, language_and_grammar] only give the numbers",
}
],
        temperature=1.0,
        max_tokens=100
    )
    print(response)
    # Extracting the scores from the response
    output_text = response.choices[0].message.content.strip()
    print('output_text', output_text)
    scores = list(map(int, output_text.strip('[]').split(',')))
    return scores


def compare_texts():
    slide_dir = './slides_text'
    audio_dir = './transcribed_texts'
    count =1
    for slide_file in os.listdir(slide_dir):
        print("count:",count)
        count = count + 1

        if slide_file.startswith('slide_') and slide_file.endswith('.txt'):
            slide_num = slide_file.split('_')[1].split('.')[0]
            print("slide_num:", slide_num )
            audio_file = None
            for f in os.listdir(audio_dir):
                if f.startswith(slide_num + '_'):
                    audio_file = f
                    break

            if audio_file:
                slide_path = os.path.join(slide_dir, slide_file)
                audio_path = os.path.join(audio_dir, audio_file)
        
                with open(slide_path, 'r') as slide_f, open(audio_path, 'r') as audio_f:
                    slide_text = slide_f.read()
                    print("slide_text:",slide_text)
                    audio_text = audio_f.read()
                    print("audio_text:",audio_text)
                scores = evaluate_presentation(slide_text, audio_text)

                store_to_awsdynamoDB(slide_num, scores)
                print(f'Saved scores for slide {slide_num}: {scores}')
                



