import React from 'react'
import ReactDOM from 'react-dom'
import { GoogleMap, LoadScript } from '@react-google-maps/api';
import MyComponent from './MapAPI'

class User extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            _id: null,
            _lat: null,
            _lon: null,
        }
    }
    set id(username){
        this.state._id = username;
    }
    set lat(latitude){
        this.state._lat = latitude;
    }
    set lon(longitude){
        this.state._lon = longitude;
    }
    get id(){
        return this.state._id;
    }
    get lat(){
        return this.state._lat;
    }
    get lon(){
        return this.state._lon;
    }
}

const center = (lat, lon) => {
    return {
        lat: lat,
        lon: lon
    }
}

function TopNav() {
    return (
        
        <div id="topnav">
            <button ></button>
        </div>
    )
}

function FirstMenu() {
    return (
        <div id="firstMenu">
            <form>
                <label for="username">Input Username: </label>
                <input type="text" id="username" name="username"></input> <br />
                <label for="zip">Input Zip Code: </label>
                <input type="text" id="zip" name="zip"></input>
            </form>
        </div>
    )
}

function Combined() {
    return (
        <div id='all'>
            <FirstMenu />
            <MyComponent />
        </div>
    )
}

export default Combined;
