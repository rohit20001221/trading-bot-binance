import { FC } from "react";
import { Text, View, StyleSheet } from "react-native";
import { AntDesign } from "@expo/vector-icons";

export type OrderItemProps = {
  status?: "buy" | "sell";
  asset?: string;
  quantity?: number;
};

const COLORS = {
  buy: "#2ecc71",
  sell: "#e74c3c",
};

const OrderItem: FC<OrderItemProps> = ({ status = "buy", asset, quantity }) => {
  return (
    <View style={styles.container}>
      <View style={{ ...styles.status, ...styles[status] }}></View>
      <View style={styles.content}>
        <Text style={{ ...styles.bold, ...styles.lg }}>
          Asset: <Text style={styles.asset}>{asset}</Text>
        </Text>
        <Text style={styles.qty}>Qty: {quantity}</Text>
      </View>
      <View style={styles.action}>
        <AntDesign name="rightcircleo" size={24} color={COLORS[status]} />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    minHeight: 80,
    borderRadius: 8,
    display: "flex",
    flexDirection: "row",
    overflow: "hidden",
    borderTopWidth: 0.4,
    borderBottomWidth: 0.4,
    borderRightWidth: 0.4,
    borderColor: "lightgray",
    backgroundColor: "white",
  },
  status: {
    flex: 0.02,
    overflow: "hidden",
  },
  content: {
    flex: 0.9,
    padding: 8,
  },
  bold: {
    fontWeight: "bold",
  },
  lg: {
    fontSize: 16,
  },
  buy: {
    backgroundColor: COLORS.buy,
  },
  sell: {
    backgroundColor: COLORS.sell,
  },
  asset: {
    color: "#7f8c8d",
  },
  qty: {
    fontSize: 12,
  },
  action: {
    flex: 0.08,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: 8,
  },
});

export default OrderItem;
