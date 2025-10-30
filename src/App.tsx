import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { DishCard } from "./components/DishCard";
import { DishPerformanceChart } from "./components/DishPerformanceChart";
import { WeakPointsChart } from "./components/WeakPointsChart";
import {
  getTopRatedDishes,
  getBottomRatedDishes,
} from "./data/mockDishes";
import { TrendingUp, TrendingDown, UtensilsCrossed } from "lucide-react";

export default function App() {
  const topDishes = getTopRatedDishes(5);
  const bottomDishes = getBottomRatedDishes(5);

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-amber-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <UtensilsCrossed className="w-8 h-8 text-orange-600" />
            <h1 className="text-orange-600">Restaurant Analytics Dashboard</h1>
          </div>
          <p className="text-muted-foreground">
            Track dish performance and identify areas for improvement
          </p>
        </div>

        {/* Top and Bottom Dishes */}
        <Tabs defaultValue="top" className="w-full mb-8">
          <TabsList className="grid w-full max-w-md mx-auto grid-cols-2">
            <TabsTrigger value="top" className="flex items-center gap-2">
              <TrendingUp className="w-4 h-4" />
              Top Rated
            </TabsTrigger>
            <TabsTrigger value="bottom" className="flex items-center gap-2">
              <TrendingDown className="w-4 h-4" />
              Needs Improvement
            </TabsTrigger>
          </TabsList>

          <TabsContent value="top" className="mt-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
              {topDishes.map((dish, index) => (
                <DishCard key={dish.id} dish={dish} rank={index + 1} />
              ))}
            </div>
          </TabsContent>

          <TabsContent value="bottom" className="mt-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
              {bottomDishes.map((dish, index) => (
                <DishCard key={dish.id} dish={dish} rank={index + 1} />
              ))}
            </div>
          </TabsContent>
        </Tabs>

        {/* Performance Analysis Charts */}
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 mb-8">
          <DishPerformanceChart />
          <WeakPointsChart />
        </div>
      </div>
    </div>
  );
}
