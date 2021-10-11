import React, {useState} from "react";
import {ActionBtn} from "./buttons";


export function ParentTweet (props) {
    const {tweet} = props
    return (
        tweet.parent ?
            <div className='row  ml-5'>
                <div className="col-12 p-3 border rounded  shadow">
                    <p className='mb-0 text-muted small'>Retweet</p>
                    <Tweet hideActions tweet={tweet.parent}/></div>
            </div> : null
    )
}


export function Tweet (props) {
    const {tweet, didRetweet, hideActions} = props
    const [actionTweet, setActionTweet] = useState (props.tweet ? props.tweet : null)

    // const isDetail = true
    const path = window.location.pathname
    var idRegex = /(?<tweetid>\d+)/
    var match = path.match (idRegex)

    var urlTweetId = match ? match.groups.tweetid : '-1'
    const isDetail = `${tweet.id}` === `${urlTweetId}`


        const handlePerformAction = (newActionTweet, status) => {
            if (status === 200) {
                setActionTweet (newActionTweet)
            } else if (status === 201) {
                //     then we let the tweet know.
                if (didRetweet) {
                    didRetweet (newActionTweet)
                }
            }
        }
        const handleLink = (event) => {
            event.preventDefault ()
            window.location.href = `/${tweet.id}/`
        }

        const className = props.className ? props.className : 'col-10  col-md-12'
        return <div className={className}>

            <p className=''>{tweet.id} - {tweet.content} </p>
            <ParentTweet tweet={tweet}/>
            <br/>
            {actionTweet && hideActions !== true && <div className='btn btn-group '>
                <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction}
                           action={{type: 'like', display: 'Likes'}}/>
                <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction}
                           action={{type: 'unlike', display: 'Unlike'}}/>
                <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction}
                           action={{type: 'retweet', display: 'Retweet'}}/>
                {isDetail === true ? null :
                    <button className='btn btn-outline-primary ' onClick={handleLink}>View</button>}
            </div>}
        </div>
    }
