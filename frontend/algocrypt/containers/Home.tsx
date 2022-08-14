import { StyleSheet, View, FlatList } from "react-native";
import { FC } from "react";
import OrderItem, { OrderItemProps } from "../components/OrderItem";
import { useNavigation } from "./NavigationContainer";

const Home: FC = () => {
  const { navigate } = useNavigation();

  return (
    <View style={styles.container}>
      <FlatList<OrderItemProps>
        data={[
          { asset: "BTCUSDT", quantity: 0.004, status: "sell" },
          { asset: "BTCUSDT", quantity: 0.004, status: "buy" },
        ]}
        renderItem={({ item, index }) => {
          return (
            <OrderItem
              {...item}
              onPress={() => navigate(`details`, { index })}
            />
          );
        }}
        ItemSeparatorComponent={() => <View style={{ height: 4 }} />}
      />
    </View>
  );
};

export default Home;

const styles = StyleSheet.create({
  container: {
    padding: 8,
    flex: 1,
  },
});
