import { FC } from "react";
import { Text, View, StyleSheet, TouchableWithoutFeedback } from "react-native";
import { AntDesign } from "@expo/vector-icons";
import { useNavigation } from "../containers/NavigationContainer";

const OrderDescription: FC = () => {
  const { navigate } = useNavigation();

  return (
    <View>
      <View style={styles.header}>
        <Text style={{ ...styles.lg, ...styles.fullFlex, ...styles.bold }}>
          Order Description
        </Text>
        <TouchableWithoutFeedback>
          <AntDesign
            onPress={() => navigate(`home`)}
            name="closecircleo"
            size={24}
            color="black"
          />
        </TouchableWithoutFeedback>
      </View>
      <View style={styles.container}>
        <Text>
          Asset: <Text>BTCUSDT</Text>
        </Text>
        <Text>
          Timestamp: <Text>{new Date().toUTCString()}</Text>
        </Text>
        <Text>
          Quantity: <Text>{10}</Text>
        </Text>
        <Text>
          Type: <Text>Sell</Text>
        </Text>
        <Text>
          Channel: <Text>ema-200-150</Text>
        </Text>
        <Text>
          Stop Loss: <Text>2345.3</Text>
        </Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  header: {
    display: "flex",
    flexDirection: "row",
    alignItems: "flex-end",
    padding: 16,
    borderBottomWidth: 1,
    borderColor: "lightgray",
  },
  lg: {
    fontSize: 20,
  },
  fullFlex: {
    flex: 1,
  },
  container: {
    paddingHorizontal: 12,
    paddingVertical: 24,
  },
  bold: {
    fontWeight: "bold",
  },
});

export default OrderDescription;
