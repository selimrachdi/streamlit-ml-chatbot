import streamlit as st
import json
from streamlit_lottie import st_lottie


from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
from joblib import load
from streamlit_option_menu import option_menu
# Function to load and display a Lottie animation
# Function to load and display a Lottie animation
def display_lottie_animation(animation_path, title, height=300, width=300, loop=True):
    # Load the JSON animation file with UTF-8 encoding
    with open(animation_path, "r", encoding="utf-8") as file:
        animation_data = json.load(file)
    
    # Display the Lottie animation
    st_lottie(animation_data, height=height, width=width, loop=loop, key=title)


# Define the allowed users and their corresponding roles
allowed_users = {
    "inventory": "77a7ac2f-8548-4c55-9c8d-36c1ca8fd789",
    "maintenance": "52029c69-519a-4dd7-9ccb-fd906e77524f",
    "orders": "ce9cb8aa-0304-4d61-816e-1133a72600a0",
    "admin": "admin",
    "sales": "8ba5daa0-6400-4ef4-80ca-a9362e02906d"
}

# Define the user passwords
user_passwords = {
    "inventory": "inventory",
    "maintenance": "maintenance",
    "orders": "orders",
    "admin": "admin",
    "sales": "sales"
}

# Load the model
loaded_model = load('models/model.joblib')
knn_model = loaded_model

# Function to get response from the LLama 2 model
def getLLamaresponse(input_text, no_words, blog_style):
    llm = CTransformers(model='models/llama-2-7b-chat.ggmlv3.q8_0.bin',
                        model_type='llama',
                        config={'max_new_tokens': 256, 'temperature': 0.01})

    template = """
        Write a blog for {blog_style} job profile for a topic {input_text}
        within {no_words} words.
            """

    prompt = PromptTemplate(input_variables=["blog_style", "input_text", 'no_words'],
                            template=template)

    response = llm(prompt.format(blog_style=blog_style, input_text=input_text, no_words=no_words))
    return response


# Function for the home page
def home_page():
    st.title("Welcome to Your Oil & Gas Assistant 🛢️")
    st.write("Your go-to tool for Oil & Gas insights and assistance.")
    
    # Display the Lottie animations next to each other
    col1, col2, col3 = st.columns(3)
    
    with col1:
        display_lottie_animation("templates/assistant.json", "Assistant Animation")
    
    with col2:
        display_lottie_animation("templates/prediction.json", "Predict Class Animation")
    
    with col3:
        display_lottie_animation("templates/dashboard.json", "Dashboard Animation")
    
    st.markdown("---")  # Add a horizontal line for visual separation
    
    st.write("Start by logging in to unlock all features.")
    
    st.markdown("---")  # Add a final horizontal line for separation
    
    st.write("For any assistance or support, contact us at support@dataminds.com")
    
    st.markdown(
        """
        <style>
        .button-css {
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-align: center;
            cursor: pointer;
        }
        .button-css:hover {
            background-color: #0056b3;
        }
        </style>
        """
        , unsafe_allow_html=True
    )


# Function for the assistant page
def assistant_page():
    st.title("Oil & Gas Assistant 🛢️")
    st.write("Get personalized assistance on various topics.")
    
    # Display the assistant animation on the assistant page
    display_lottie_animation("templates/assistant.json", "")
    
    input_text = st.text_input("Enter the Assistance Topic")
    no_words = st.text_input('No of Words')
    blog_style = st.selectbox('Writing the assistance as', ('Industrial expert', 'Data Scientist', 'IT Expert'), index=0)
    submit = st.button("Generate")
    if submit:
        st.write(getLLamaresponse(input_text, no_words, blog_style))


# Function for the dashboard page
def dashboard_page():
    st.title("Oil & Gas Dashboard 🛢️")
    display_lottie_animation("templates/dashboard.json", "")
    
    user = st.session_state.get("user")
    
    if not user:
        st.error("You are not logged in. Please log in to access the dashboard.")
    elif user in allowed_users:
        if user == "admin":
            selected_dashboard = st.selectbox("Select Dashboard", ["Inventory", "Maintenance", "Orders", "Sales"])
            
            if selected_dashboard == "Inventory":
                st.components.v1.iframe(
                    "https://app.powerbi.com/reportEmbed?autoAuth=true&ctid=604f1a96-cbe8-43f8-abbf-f8eaf5d85730&reportId=77a7ac2f-8548-4c55-9c8d-36c1ca8fd789",
                    height=800,
                    width=1200
                )
            elif selected_dashboard == "Maintenance":
                st.components.v1.iframe(
                    "https://app.powerbi.com/reportEmbed?autoAuth=true&ctid=604f1a96-cbe8-43f8-abbf-f8eaf5d85730&reportId=52029c69-519a-4dd7-9ccb-fd906e77524f",
                    height=800,
                    width=1200
                )
            elif selected_dashboard == "Orders":
                st.components.v1.iframe(
                    "https://app.powerbi.com/reportEmbed?autoAuth=true&ctid=604f1a96-cbe8-43f8-abbf-f8eaf5d85730&reportId=ce9cb8aa-0304-4d61-816e-1133a72600a0",
                    height=800,
                    width=1200
                )
            elif selected_dashboard == "Sales":
                st.components.v1.iframe(
                    "https://app.powerbi.com/reportEmbed?autoAuth=true&ctid=604f1a96-cbe8-43f8-abbf-f8eaf5d85730&reportId=8ba5daa0-6400-4ef4-80ca-a9362e02906d",
                    height=800,
                    width=1200
                )
        else:
            st.components.v1.iframe(
                f"https://app.powerbi.com/reportEmbed?autoAuth=true&ctid=604f1a96-cbe8-43f8-abbf-f8eaf5d85730&reportId={allowed_users[user]}",
                height=800,
                width=1200
            )
    else:
        st.error("You do not have access to this dashboard.")
import base64
def set_local_image_as_background(image_path):
    with open(image_path, "rb") as f:
        image_data = f.read()
        image_base64 = base64.b64encode(image_data).decode()

    st.markdown(
        f"""
        <style>
        .reportview-container {{
            background: url(data:image/jpeg;base64,{image_base64});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )




# Function for the predict class page
def predict_class_page():
    st.title("Predict Class 🤖")
    
    # Display the prediction animation on the predict class page
    display_lottie_animation("templates/prediction.json", "")

    # Input fields for each feature
    gross_totalizer = st.number_input("GROSS_TOTALIZER", value=0.0)
    gross_thruput = st.number_input("GROSS_THRUPUT", value=0.0)
    net_totalizer = st.number_input("NET_TOTALIZER", value=0.0)
    net_thruput = st.number_input("NET_THRUPUT", value=0.0)
    bod_gross_totalizer = st.number_input("BOD_GROSS_TOTALIZER", value=0.0)
    bod_net_totalizer = st.number_input("BOD_NET_TOTALIZER", value=0.0)

    predict_button = st.button("Predict")

    if predict_button:
        # Prepare the input features
        features = [[gross_totalizer, gross_thruput, net_totalizer, net_thruput, bod_gross_totalizer, bod_net_totalizer]]

        # Make prediction using the KNN model
        prediction = knn_model.predict(features)

        # Determine the product class based on the prediction
        product_class = "Product 4" if prediction[0] == 0 else "Product 7"

        # Display the predicted product class
        st.write(f"Predicted Product Class: {product_class}")

import json
import streamlit as st
from streamlit_lottie import st_lottie


# Create a login page


def login_page():
    st.title("Login")
    
    # Display the home animation on the login page, centered
    display_lottie_animation("templates/home.json", "Welcome Animation", width=800)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    login_button = st.button("Login")

    if login_button:
        if username in allowed_users:
            if password == user_passwords[username]:
                st.success(f"Welcome, {username}! You are logged in as {username}.")
                st.session_state.logged_in = True
                st.session_state.user = username
            else:
                st.error("Invalid password. Please try again.")
        else:
            st.error("Invalid username. Please try again.")



def custom_navigation_bar():
    options = ["Home", "Assistant", "Predict Class", "Dashboard", "Logout"]
    icons = ["home", "user", "chart-line", "chart-bar", "sign-out-alt"]

    selected = option_menu(
        menu_title=None,  # No title
        options=options,  # Menu options
        icons=icons,  # Optional icons
        menu_icon="bars",  # Menu icon
        default_index=0,  # Default selected index
        orientation="horizontal",  # Display horizontally
        styles={
            "container": {"padding": "10px", "background-color": "#f0f0f0"},
            "icon": {"color": "#333", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0 10px", "--hover-color": "#ddd"},
            "nav-link-selected": {"background-color": "#007bff", "color": "#fff"},
        },
    )

    return selected
def main():
    st.set_page_config(page_title="PGS Assistant App", page_icon="🛢️", layout="wide")
        # Set the background image
        # Set the local image path
    local_image_path = "templates/template.jpg"
    
    # Set the local image as the background
    set_local_image_as_background(local_image_path)


    
    st.markdown(
        """
        <style>
        .stApp {
            width: 100%;
            max-width: none;
            padding: 0;
        }
        </style>
        """
        , unsafe_allow_html=True
    )

    if not st.session_state.get("logged_in"):
        login_page()
    else:
        selected = custom_navigation_bar()

        if selected == "Home":
            home_page()
        elif selected == "Assistant":
            assistant_page()
        elif selected == "Predict Class":
            predict_class_page()
        elif selected == "Dashboard":
            dashboard_page()
        elif selected == "Logout":
            st.session_state["logged_in"] = False
            st.experimental_rerun()



if __name__ == "__main__":
    main()
