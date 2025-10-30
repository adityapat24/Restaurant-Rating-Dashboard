import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { getBottomRatedDishes } from "../data/mockDishes";

export function WeakPointsChart() {
  const bottomDishes = getBottomRatedDishes(7);

  const chartData = bottomDishes.map((dish) => ({
    name: dish.name.length > 15 ? dish.name.substring(0, 15) + "..." : dish.name,
    Taste: dish.ratings.taste,
    Texture: dish.ratings.texture,
    "Bang for Buck": dish.ratings.bangForBuck,
  }));

  return (
    <Card>
      <CardHeader>
        <CardTitle>Rating Breakdown: Dishes Needing Attention</CardTitle>
        <p className="text-sm text-muted-foreground">
          Identify which specific aspects need improvement
        </p>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={chartData} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" domain={[0, 5]} />
            <YAxis type="category" dataKey="name" width={120} />
            <Tooltip />
            <Legend />
            <Bar dataKey="Taste" fill="#ef4444" />
            <Bar dataKey="Texture" fill="#3b82f6" />
            <Bar dataKey="Bang for Buck" fill="#10b981" />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
