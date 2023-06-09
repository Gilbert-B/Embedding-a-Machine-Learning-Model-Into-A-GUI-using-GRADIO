import gradio as gr
import pandas as pd
import pickle


# Load the pipeline using pickle
with open(r'C:\Users\GilB\OneDrive\Documents\Git Repo\ML-App\Embedding-a-Machine-Learning-Model-Into-A-GUI\pipeline.pkl', 'rb') as f:
    pipeline = pickle.load(f)

def predict(Gender,TotalCharges, tenure, MonthlyCharges, PaymentMethod_Electronic_check, InternetService_Fiber_optic, Contract_Two_year, OnlineSecurity_Yes, PaperlessBilling_Yes, Partner_Yes):
    input_list = [Gender, TotalCharges, tenure, MonthlyCharges, PaymentMethod_Electronic_check, InternetService_Fiber_optic, Contract_Two_year, OnlineSecurity_Yes, PaperlessBilling_Yes, Partner_Yes]

        # Check if any of the input values are strings ('Yes' or 'No')
    for i, val in enumerate(input_list):
        if isinstance(val, str):
            if val.lower() == "yes" or "male":
                input_list[i] = True
            elif val.lower() == "no" or "female":
                input_list[i] = False
            elif not isinstance(val, (int, float)):
                return "Error: Input value must be 'Yes' or 'No' or numeric"
            else:
                input_list[i] = float(val)
        # Convert 'Yes'/'No' values to boolean
        input_df = pd.DataFrame([input_list], columns=['TotalCharges', 'tenure', 'MonthlyCharges', 'PaymentMethod_Electronic_check', 'InternetService_Fiber_optic', 'Contract_Two_year', 'gender_Male', 'OnlineSecurity_Yes', 'PaperlessBilling_Yes', 'Partner_Yes'])
    
    prediction = pipeline['model'].predict(input_df)
    pred_proba = pipeline['model'].predict_proba(input_df)[0]
    
    # Create a dataframe to display the prediction and confidence score
    pred_df = pd.DataFrame({'class': pipeline.classes_,
                            'confidence': pred_proba})
    # Sort the dataframe by confidence score in descending order
    pred_df = pred_df.sort_values('confidence', ascending=False)
    return pred_df

# Define the Gradio interface
input_interface =  [
    
        gr.inputs.Radio(['Male','Female'], label="Gender"),
        gr.inputs.Slider(minimum=0, maximum=2000, default=50, label= "Total Charges"),
        gr.inputs.Slider(minimum=0, maximum=50, default=5, label="Tenure"),
        gr.inputs.Slider(minimum=0, maximum=500, default=20, label="Monthly Charges"),
        gr.inputs.Radio(['Yes','No'], label="Electronic check Payment"),
        gr.inputs.Radio(['Yes','No'], label="Fiber optic Internet Service"),
        gr.inputs.Dropdown(["Month-to-month", "One year", "Two year"], label="Contract"),
        gr.inputs.Checkbox(label="Online Security"),
        gr.inputs.Checkbox(label="Paperless Billing"),
        gr.inputs.Checkbox(label="Partner")
]



    
label=pipeline['label']

output_table = gr.outputs.Dataframe(headers=['churn', 'confidence'],type='pandas')

# Create the Gradio app
banner_html = "<img src='https://cdn-dfnaj.nitrocdn.com/xxeFXDnBIOflfPsgwjDLywIQwPChAOzV/assets/images/optimized/rev-509f30c/wp-content/uploads/2017/07/customer-churn-edit.jpeg' style='display: block; margin: auto; max-width: 100%; max-height: 400px;'>"
gr.Interface ( fn=predict, inputs=input_interface, outputs=output_table,type="tabs",title="Churn Prediction App", description=banner_html, theme="dark", layout="vertical", interface_name="My Churn Prediction App",font="sans-serif").launch()