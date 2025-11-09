import streamlit as st

st.title("Model Overview")

st.markdown(''' This section provides a general explanation of the computational model used, aiming to clarify the notations, data sources, input fields, where the data comes from, and how the model operates.  
            It is important to note that this explanation is based on a generic version of the model for illustrative purposes. For deeper understanding and complete technical details, we invite users to visit our repository.  
            Contrary to how information is displayed on the website, the following diagram illustrates how the input data is requested from the user, showing which parameters are needed to operate the tool.  
            The abbreviations stand for:  

            The user is required to provide the following data:  

            The variables x, y, z are retrieved directly from the database, and a, b, c may also be obtained from the database at the user’s discretion.  
            These inputs are returned to the computational function, generating accumulated yearly values for both GHG emissions and TCO. These results are stored in a list, which serves as the basis for the charts rendered on the results page of the platform.  
            **About the emissions calculation:**  
            **About the total cost of ownership calculation:**  

            We again emphasize the importance of consulting the models available in our repository for clarification of any questions, as each category follows a specific set of equations and assumptions—especially regarding emissions calculations.''')

