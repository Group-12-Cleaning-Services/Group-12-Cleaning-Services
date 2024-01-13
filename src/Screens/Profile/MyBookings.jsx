import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, StatusBar, SafeAreaView } from 'react-native';
import { Feather } from '@expo/vector-icons';
import { bookings } from '../../../Data';
import { SIZES } from '../../Constants/Theme';

export default function MyBookings({navigation}) {

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.gobackArrow}>
        <Feather name="arrow-left" size={24}
         color="black" onPress={()=>navigation.goBack()} />
      </View>
      {/* <View style={styles.tabContainer}>
        <TouchableOpacity style={styles.activeButtonContainer}>
          <Text style={styles.tabButtonText}>Active</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.successButtonContainer}>
          <Text style={styles.tabButtonText}>Success</Text>
        </TouchableOpacity>
      </View> */}
      <View style={styles.MyBookingsTextContainer}>
        <Text style={styles.MyBookingsText}>My Bookings</Text>
      </View>
      <ScrollView style={styles.bookingList}>
        {bookings.map((booking, index) => (
          <View key={index} style={styles.bookingCard}>
            <Text style={styles.bookingId}>{booking.id}</Text>
            <Text style={[{color:booking.color},styles.bookingStatus]}>{booking.status}</Text>
            <Text style={styles.bookingName}>{booking.name}</Text>
            <Text style={styles.bookingDate}>{booking.date}</Text>
            <Text style={styles.bookingPrice}>{booking.price}</Text>
            <View style={styles.border}></View>
            <Text style={styles.bookingCompany}>{booking.company}</Text>
            {booking.action && (
              <TouchableOpacity style={styles.bookingActionButton}>
                <Text style={styles.bookingActionButtonText}>{booking.action}</Text>
              </TouchableOpacity>
            )}
          </View>
        ))}
      </ScrollView>
      <TouchableOpacity style={styles.homeButton}>
        <Feather name="home" size={24} color="black" onPress={() => navigation.navigate("Home")} />
      </TouchableOpacity>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#B3CDE0",
  },
  gobackArrow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingTop:SIZES.height*0.05,
    paddingLeft:SIZES.height*0.03
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  tabContainer: {
    flexDirection: 'row',
    paddingBottom:10,
    backgroundColor:"rgba(32, 35, 37, 1)",
    borderRadius:15,
    margin:10,
    justifyContent:"space-around",
    alignItems:"center"
  },
  MyBookingsTextContainer:{
    alignItems:"center",
    justifyContent:"center",
    paddingBottom:SIZES.height*0.02
  },
  MyBookingsText:{
    fontSize:SIZES.width*0.07
  },
  activeButton: {
    backgroundColor: '#d1d1d1',
    width:120,
    padding:7,
    borderRadius: 20,
    marginHorizontal: 5,
    alignItems:'center'
  },
  tabButtonText: {
    color: '#ffffff',
  },
  bookingList: {
    flex: 1,
  },
  bookingCard: {
    margin: 10,
    padding: 15,
    borderRadius: 10,
    borderColor: 'rgba(100, 151, 177, 1)',
    borderWidth: 0.5,
  },
  bookingId: {
    fontWeight: 'bold',
  },
  bookingStatus: {
    alignSelf: 'flex-end',
    backgroundColor: '#ffff',
    padding: 7,
    borderRadius: 20,
  },
  bookingName: {
    fontSize: 16,
    fontWeight: 'bold',
    marginTop: 5,
  },
  bookingDate: {
    color: '#555',
  },
  bookingPrice: {
    color: '#555',
  },
  bookingCompany: {
    color: '#555',
    marginBottom: 10,
  },
  border:{
    borderTopWidth:0.5,
    borderColor: 'rgba(100, 151, 177, 1)',
    marginTop:10,
    marginBottom:10  
},
  bookingActionButton: {
    borderWidth: 1,
    borderColor: 'red',
    padding: 10,
    borderRadius: 20,
    alignItems: 'center',
  },
  bookingActionButtonText: {
    color: 'red',
  },
  homeButton: {
    position: 'absolute',
    bottom: 20,
    right: 20,
    backgroundColor: '#ffffff',
    padding: 15,
    borderRadius: 30,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
});