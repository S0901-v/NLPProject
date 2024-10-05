import gradio as gr
import pandas as pd
from theme_classifier import ThemeClassifier

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

# Main Gradio interface function
def main():
    with gr.Blocks() as iface:
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
                            
    iface.launch(share=True)


# Run the app
if __name__ == "__main__":
    main()