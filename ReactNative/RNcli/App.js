import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import Info from './src/Info';

const App = () => {
  return(
    <View  style={styles.conatiner}>
      <Text>MainScreen</Text>
    </View>
  );
}

const style = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'cneter',
    justifyContent: 'center',
  }
});

export default App;