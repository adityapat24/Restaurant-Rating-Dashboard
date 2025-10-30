import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ZAxis,
  Cell,
} from "recharts";
import { dishes, calculateAverageRating } from "../data/mockDishes";

export function DishPerformanceChart() {
  const chartData = dishes.map((dish) => ({
    name: dish.name,
    rating: calculateAverageRating(dish),
    reviews: dish.reviewCount,
  }));

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-semibold">{payload[0].payload.name}</p>
          <p className="text-sm">Rating: {payload[0].payload.rating}</p>
          <p className="text-sm">Reviews: {payload[0].payload.reviews}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Dish Performance: Rating vs Review Count</CardTitle>
        <p className="text-sm text-muted-foreground">
          Lower left quadrant = High priority for improvement (low rating, many reviews)
        </p>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={400}>
          <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              type="number"
              dataKey="reviews"
              name="Review Count"
              label={{ value: "Review Count", position: "insideBottom", offset: -10 }}
            />
            <YAxis
              type="number"
              dataKey="rating"
              name="Average Rating"
              domain={[0, 5]}
              label={{ value: "Average Rating", angle: -90, position: "insideLeft" }}
            />
            <ZAxis range={[100, 400]} />
            <Tooltip content={<CustomTooltip />} />
            <Scatter data={chartData}>
              {chartData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={entry.rating < 3.5 ? "#ef4444" : entry.rating < 4.2 ? "#f59e0b" : "#10b981"}
                />
              ))}
            </Scatter>
          </ScatterChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
