import { View, BackHandler } from "react-native";
import { FC, useEffect } from "react";
import { useNavigation } from "./NavigationContainer";
import OrderDescription from "../components/OrderDescription";

const OrderDetail: FC = () => {
  const { params, navigate } = useNavigation();
  const { index } = params as Record<string, number>;

  useEffect(() => {
    const handler = BackHandler.addEventListener("hardwareBackPress", () => {
      navigate(`home`);

      return true;
    });

    return () => handler.remove();
  }, []);

  return (
    <View>
      <OrderDescription />
    </View>
  );
};

export default OrderDetail;
