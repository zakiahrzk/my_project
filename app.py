import streamlit as st
import pickle


def main():
    bg = """<div style='background-color:black; padding:13px'>
              <h1 style='color:black'>Time Series Forecasting</h1>
       </div>"""
    st.markdown(bg, unsafe_allow_html=True) #reading the variable bg using streamlit

    left, right = st.columns((2,2)) #dividing your interface to 2 sections

    #Show all the independent columns along with the label for each column and the values in that column"

    #Example
    timestamp = left.number.input("Period in months")
    button = st.button('Predict')
    '''

    # if button is clicked
    if button:
        # make prediction
        result = predict(timestamp)
        st.success(f'The predicted attrition rate is {result}')

# load the train model
with open('attrition_model.pkl', 'rb') as pkl:
    attrition_model = pickle.load(pkl)

'''Example for predict function


def predict(timestamp):
    # making predictions
    prediction = attrition_model.predict([[timestamp]])
    
    verdict = prediction
    return verdict

'''


if __name__ == '__main__':
    main()
