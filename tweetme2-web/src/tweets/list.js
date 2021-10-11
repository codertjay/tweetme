/* this is the list of all tweets and in here we made the callback
* from our load tweets function */
import React, {useEffect, useState} from "react";
import {apiTweetsList} from "./lookup";
import {Tweet} from "./detail";


export function TweetList (props) {
    const [tweetsInit, setTweetsInit] = useState ([])
    const [tweets, setTweets] = useState ([])
    const [tweetsDidSet, setTweetsDidSet] = useState (false);

    // this useEffect is for the tweet i am passing in from the form
    useEffect (() => {
        const final = [...props.newTweets].concat (tweetsInit)
        if (final.length !== tweets.length) {
            setTweets (final)
        }
    }, [props.newTweets, tweets, tweetsInit])

    useEffect (() => {
        if (tweetsDidSet === false) {
            //  callback function from the xmlhttprequest
            const handleTweetListLookup = (response, status) => {
                if (status === 200) {
                    // we use the call back to set the tweets response
                    setTweetsInit (response)
                    setTweetsDidSet (true)
                } else {
                    alert ("There was an error ")
                }
            }
            apiTweetsList (props.username, handleTweetListLookup)
        }
    }, [tweetsInit, props.username, tweetsDidSet, setTweetsDidSet])

    const handleDidRetweet = (newTweet) => {
        const updateTweetsInit = [...tweetsInit]
        updateTweetsInit.unshift (newTweet)
        setTweetsInit (updateTweetsInit)

        const updateFinalInit = [...tweets]
        updateFinalInit.unshift (tweets)
        setTweets (updateTweetsInit)
        console.log (tweets)

    }

    return (
        <div>
            {tweets.map ((item, index) => {
                return <Tweet key={index} tweet={item}
                              didRetweet={handleDidRetweet}
                              className='my-5 py-5 shadow bg-light  text-dark'/>
            })}
        </div>
    )
}
