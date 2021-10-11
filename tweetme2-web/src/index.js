import React from 'react';
import ReactDOM from 'react-dom';
// import App from './App';
import * as serviceWorker from './serviceWorker';
import 'bootstrap/dist/css/bootstrap.css';
import {TweetsComponent, TweetDetailComponent} from "./tweets";


// const appEl = document.getElementById ('root')

// if (appEl){
//     ReactDOM.render( <App />, appEl)
// }


const e = React.createElement
const component = document.getElementById ('tweetme2')
console.log (component)
if (component) {
    ReactDOM.render (e (TweetsComponent, component.dataset),
        component);
}

const tweetDetailElements = document.querySelectorAll ("#tweetme-2-detail")
tweetDetailElements.forEach (container => {
    ReactDOM.render (
        e (TweetDetailComponent, container.dataset),
        container);
})

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister ();
