import { StyleSheet, View, FlatList } from "react-native";
import { FC } from "react";
import OrderItem, { OrderItemProps } from "../components/OrderItem";

const Home: FC = () => {
  return (
    <View style={styles.container}>
      <FlatList<OrderItemProps>
        data={[]}
        renderItem={({ item }) => {
          return <OrderItem {...item} />;
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
