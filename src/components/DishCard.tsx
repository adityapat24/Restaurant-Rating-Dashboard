import { Card, CardContent } from "./ui/card";
import { Star } from "lucide-react";
import { Dish, calculateAverageRating } from "../data/mockDishes";
import { ImageWithFallback } from "./figma/ImageWithFallback";

interface DishCardProps {
  dish: Dish;
  rank?: number;
}

export function DishCard({ dish, rank }: DishCardProps) {
  const avgRating = calculateAverageRating(dish);

  return (
    <Card className="overflow-hidden hover:shadow-lg transition-shadow">
      <div className="relative h-40 overflow-hidden">
        <ImageWithFallback
          src={dish.image}
          alt={dish.name}
          className="w-full h-full object-cover"
        />
        {rank && (
          <div className="absolute top-2 left-2 bg-black/70 text-white rounded-full w-8 h-8 flex items-center justify-center">
            #{rank}
          </div>
        )}
      </div>
      <CardContent className="p-4">
        <div className="flex justify-between items-start mb-2">
          <div>
            <h3 className="font-semibold">{dish.name}</h3>
            <p className="text-sm text-muted-foreground">${dish.price}</p>
          </div>
          <div className="flex items-center gap-1">
            <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
            <span className="font-semibold">{avgRating}</span>
          </div>
        </div>
        <div className="space-y-1 mt-3">
          <div className="flex justify-between items-center text-sm">
            <span className="text-muted-foreground">Taste</span>
            <span className="font-medium">{dish.ratings.taste}</span>
          </div>
          <div className="flex justify-between items-center text-sm">
            <span className="text-muted-foreground">Texture</span>
            <span className="font-medium">{dish.ratings.texture}</span>
          </div>
          <div className="flex justify-between items-center text-sm">
            <span className="text-muted-foreground">Bang for Buck</span>
            <span className="font-medium">{dish.ratings.bangForBuck}</span>
          </div>
        </div>
        <p className="text-xs text-muted-foreground mt-3">
          {dish.reviewCount} reviews
        </p>
      </CardContent>
    </Card>
  );
}
