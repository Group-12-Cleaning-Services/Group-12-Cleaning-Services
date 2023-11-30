import React from 'react';
import Home from '../Screens/Home/Home';
import Login from '../Screens/Authentication/Login';
import Register from '../Screens/Authentication/Register';
import OrgRegister from '../Screens/Authentication/OrgRegister';
import ResetPassword from "../Screens/Authentication/ResetPassword"
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import BookingsScreen from '../Screens/Profile/SeeBookings';
import OTPVerification from "../Screens/Authentication/OTPVerification"
import { StatusBar } from 'expo-status-bar';
import Laundry from '../Screens/Home/Laundry';


const Tabs = () => {
    const Stack = createNativeStackNavigator()
  return (
    <NavigationContainer>
        <Stack.Navigator initialRouteName='Home'
        screenOptions={{
            headerShown:false
        }}
        >
            <Stack.Screen name='Home' component={Home} options={{statusBarColor:"#42322E"}}/>
            <Stack.Screen name='Laundry' component={Laundry} options={{ statusBarColor: '#171717', statusBarStyle:"white" }}/>
            <Stack.Screen name='Register' component={Register} options={{ statusBarColor: '#B3CDE0', statusBarStyle:"dark" }}/>
            <Stack.Screen name='Login' component={Login} options={{statusBarColor:"#040268" }}/>
            <Stack.Screen name='OrgRegister' component={OrgRegister} options={{ statusBarColor: '#B3CDE0', statusBarStyle:"dark" }}/>
            <Stack.Screen name='ResetPassword' component={ResetPassword} options={{ statusBarColor: '#B3CDE0', statusBarStyle:"dark" }}/>
            <Stack.Screen name='Bookings' component={BookingsScreen} options={{ statusBarColor: '#FF5733' }}/>
            <Stack.Screen name='OTP' component={OTPVerification} options={{ statusBarColor: 'black', statusBarStyle:"white" }}/>
        </Stack.Navigator>
    </NavigationContainer>
  )
}

export default Tabs