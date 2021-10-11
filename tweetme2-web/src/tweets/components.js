import React, {useEffect, useState} from "react";
import {TweetList} from './list'
import {TweetCreate} from "./create";
import {apiTweetDetail} from "./lookup";
import {Tweet} from "./detail";


export function TweetsComponent (props) {
    console.log ('The props', props)
    const [newTweets, setNewTweets] = useState ([])
    const canTweet = props.canTweet === 'false' ? false : true

    const handleNewTweet = (newTweet) => {
        // backend api response

        let tempNewTweet = [...newTweets]
        setNewTweets (newTweet)
        tempNewTweet.unshift (newTweet)
    }


    return <div className={props.className}>
        {canTweet === true &&
        <TweetCreate className='col-12 mb-3' didTweet={handleNewTweet}/>}
        <TweetList newTweets={newTweets} {...props}/>
    </div>
}

export function TweetDetailComponent (props) {
    const {tweetId} = props
    console.log (props)
    const [didLookup, setDidLookup] = useState (false)
    const [tweet,setTweet] = useState(null)
    console.log ('tweetId',tweetId)
    const handleBackendLookup = (response, status) => {
        if (status === 200){
            setTweet(response)
        }else {
            alert('There was an error finding your tweet ')
        }

    }

    useEffect (() => {
        if (didLookup === false) {
            apiTweetDetail (tweetId,handleBackendLookup)
            setDidLookup (true)
        }
    }, [didLookup,tweetId, setDidLookup])
    return (
        tweet === null ? null :
            <Tweet tweet={tweet} className={props.classname} />
    )

}



