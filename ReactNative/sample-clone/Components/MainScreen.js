import react, { Component } from 'react';
import { StyleSheet, Platform } from 'react-native';

export default class MainScreen extends Component {
    render() {
        return (
            <View style={StyleSheet.container}>
                <Text>MainScreen</Text>
            </View>
        );
    }
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
    },
});