import React from "react";
import {apiTweetsCreate} from "./lookup";

export function TweetCreate (props) {
    const textAreaRef = React.createRef ()
    console.log ('The props', props)
    const {didTweet} = props
    const handleCallbackendUpdate = (response, status) => {
        // backend api response
        console.log ('status', status)
        if (status === 201) {
            didTweet (response)
        } else {
            console.log (response)
            alert ('An error occured please try again ')
        }
    }
    const handleSubmit = (event) => {
        event.preventDefault ()
        console.log (event)
        console.log (textAreaRef.current.value)
        // backend api request
        const newVal = textAreaRef.current.value
        apiTweetsCreate (newVal, handleCallbackendUpdate)
        textAreaRef.current.value = ''
    }

    return <div className={props.className}>
        <form onSubmit={handleSubmit}>
            <textarea ref={textAreaRef} required={true} className='form-control '/>
            <button type='submit' className='btn btn-primary my-3' name='tweet'>
                Tweet
            </button>
        </form>
    </div>

}
