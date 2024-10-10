import gradio as gr
from theme_classifier import ThemeClassifier
from character_network import NamedEntityRecognizer, CharacterNetworkGenerator
from text_classification import JutsuClassifier
from dotenv import load_dotenv
import os
load_dotenv()


# Define the function to get themes
def get_themes(theme_list_str, subtitles_path, save_path):
        theme_list = [theme.strip() for theme in theme_list_str.split(",")]
        
        print("Initializing ThemeClassifier...")
        theme_classifier = ThemeClassifier(theme_list)
        
        print(f"Getting themes from {subtitles_path}...")
        output_df = theme_classifier.get_themes(subtitles_path, save_path)

        print("Raw output from get_themes:")
        print(output_df)

        # Remove 'dialogue' from the theme list
        theme_list = [theme for theme in theme_list if theme != "dialogue"]

        output_df = output_df[theme_list]
        output_df = output_df.sum().reset_index()
        output_df.columns = ["theme", "score"]

        output_chart = gr.BarPlot(
            output_df,
            x="theme",
            y="score",
            title="Series themes",
            tooltip=["theme", "score"],
            vertical=False,
            width=500,
            height=260
        )

        return output_chart

def get_character_network(subtitles_path, ner_path):
    ner = NamedEntityRecognizer()
    ner_df = ner.get_ners(subtitles_path, ner_path)

    character_network_generator = CharacterNetworkGenerator()
    relationship_df = character_network_generator.generate_character_network(ner_df)
    html = character_network_generator.draw_network_graph(relationship_df)

    return html

def classify_text(text_classification_model_path, text_classification_data_path, text_to_classify):
    jutsu_classifier = JutsuClassifier(model_path = text_classification_model_path,
                                       data_path = text_classification_data_path,
                                       huggingface_token = os.getenv("huggingface_token")
                                       )
    output = jutsu_classifier.classify_jutsu(text_to_classify)
    output = output[0]
    return output

# Main Gradio interface function
def main():
    with gr.Blocks() as iface:
        #Theme Classification Section
        with gr.Row():
            with gr.Column():
                gr.HTML("<h1>Theme Classification (Zero shot classifier)</h1>")
                with gr.Row():
                    with gr.Column():
                        plot = gr.BarPlot(show_label=False)
                    with gr.Column():
                        theme_list = gr.Textbox(label="Themes")
                        subtitles_path = gr.Textbox(label="Subtitles or script path")
                        save_path = gr.Textbox(label="Save Path")
                        
                        get_themes_button = gr.Button("Get Themes")
                        get_themes_button.click(
                            fn=get_themes,
                            inputs=[theme_list, subtitles_path, save_path],
                            outputs=[plot]
                        )
        #Character Network Section
        with gr.Row():
            with gr.Column():
                gr.HTML("<h1>Character Network (NERs and Graphs)</h1>")
                with gr.Row():
                    with gr.Column():
                        network_html = gr.HTML()
                    with gr.Column():
                        subtitles_path = gr.Textbox(label="Subtitles or script path")
                        ner_path = gr.Textbox(label="NERs save path")
                        get_network_graph_button = gr.Button("Get character network")
                        get_network_graph_button.click(fn=get_character_network, inputs=[subtitles_path, ner_path],outputs=[network_html]) 

        #Text Classification with llms
                with gr.Row():
                    with gr.Column():
                        gr.HTML("<h1>Text classifications with LLMs</h1>")
                        with gr.Row():
                            with gr.Column():
                                text_classification_output = gr.Textbox(label="Text Classification output")
                            with gr.Column():
                                text_classification_model_path = gr.Textbox(label="Model path")
                                text_classification_data_path = gr.Textbox(label="Data path")
                                text_to_classify = gr.Textbox(label="Text input")
                                classify_text_button = gr.Button("Classify text (Jutsu)")
                                classify_text_button.click(fn=classify_text, inputs=[text_classification_model_path, text_classification_data_path, text_to_classify],outputs=[text_classification_output])  


    iface.launch(share=True)


# Run the app
if __name__ == "__main__":
    main()