import {backendLookup} from "../lookup";



export function apiTweetsAction (tweetId, action, callback) {
    const data = {id: tweetId, action:action}
    backendLookup ('POST', '/tweets/action/',
        callback, data )
}

export function apiTweetsCreate (newTweet, callback) {
    backendLookup ('POST', '/tweets/create/', callback,
        {content: newTweet})
}

export function apiTweetDetail (tweetId, callback) {
     const  endpoint = `/tweets/${tweetId}/`
    backendLookup ('GET', endpoint, callback)
}



export function apiTweetsList (username, callback) {
    let endpoint = '/tweets/'
    if (username){
        endpoint = `/tweets/?username=${username}`
    }
    backendLookup ('GET', endpoint, callback)
}










