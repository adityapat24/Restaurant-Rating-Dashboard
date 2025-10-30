export interface Dish {
  id: number;
  name: string;
  price: number;
  ratings: {
    taste: number;
    texture: number;
    bangForBuck: number;
  };
  reviewCount: number;
  image: string;
}

export const dishes: Dish[] = [
  {
    id: 1,
    name: "Truffle Mushroom Risotto",
    price: 28,
    ratings: {
      taste: 4.8,
      texture: 4.7,
      bangForBuck: 4.2,
    },
    reviewCount: 156,
    image: "https://images.unsplash.com/photo-1476124369491-e7addf5db371?w=400&h=300&fit=crop",
  },
  {
    id: 2,
    name: "Grilled Salmon",
    price: 32,
    ratings: {
      taste: 4.6,
      texture: 4.8,
      bangForBuck: 4.0,
    },
    reviewCount: 203,
    image: "https://images.unsplash.com/photo-1485921325833-c519f76c4927?w=400&h=300&fit=crop",
  },
  {
    id: 3,
    name: "Margherita Pizza",
    price: 16,
    ratings: {
      taste: 4.9,
      texture: 4.6,
      bangForBuck: 4.9,
    },
    reviewCount: 342,
    image: "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400&h=300&fit=crop",
  },
  {
    id: 4,
    name: "Caesar Salad",
    price: 12,
    ratings: {
      taste: 3.8,
      texture: 3.5,
      bangForBuck: 3.2,
    },
    reviewCount: 128,
    image: "https://images.unsplash.com/photo-1546793665-c74683f339c1?w=400&h=300&fit=crop",
  },
  {
    id: 5,
    name: "Chocolate Lava Cake",
    price: 10,
    ratings: {
      taste: 4.7,
      texture: 4.5,
      bangForBuck: 4.3,
    },
    reviewCount: 267,
    image: "https://images.unsplash.com/photo-1624353365286-3f8d62daad51?w=400&h=300&fit=crop",
  },
  {
    id: 6,
    name: "Beef Burger",
    price: 18,
    ratings: {
      taste: 4.4,
      texture: 4.2,
      bangForBuck: 4.5,
    },
    reviewCount: 412,
    image: "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400&h=300&fit=crop",
  },
  {
    id: 7,
    name: "Tomato Soup",
    price: 8,
    ratings: {
      taste: 3.2,
      texture: 2.9,
      bangForBuck: 3.0,
    },
    reviewCount: 89,
    image: "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400&h=300&fit=crop",
  },
  {
    id: 8,
    name: "Tiramisu",
    price: 12,
    ratings: {
      taste: 4.5,
      texture: 4.6,
      bangForBuck: 4.1,
    },
    reviewCount: 198,
    image: "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=400&h=300&fit=crop",
  },
  {
    id: 9,
    name: "Fish Tacos",
    price: 14,
    ratings: {
      taste: 3.5,
      texture: 3.3,
      bangForBuck: 3.4,
    },
    reviewCount: 145,
    image: "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?w=400&h=300&fit=crop",
  },
  {
    id: 10,
    name: "Lobster Bisque",
    price: 22,
    ratings: {
      taste: 4.6,
      texture: 4.4,
      bangForBuck: 3.8,
    },
    reviewCount: 176,
    image: "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400&h=300&fit=crop",
  },
  {
    id: 11,
    name: "Garlic Bread",
    price: 6,
    ratings: {
      taste: 2.8,
      texture: 2.5,
      bangForBuck: 2.7,
    },
    reviewCount: 94,
    image: "https://images.unsplash.com/photo-1573140401552-388e3c0b4972?w=400&h=300&fit=crop",
  },
  {
    id: 12,
    name: "Panna Cotta",
    price: 11,
    ratings: {
      taste: 4.3,
      texture: 4.4,
      bangForBuck: 4.0,
    },
    reviewCount: 132,
    image: "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400&h=300&fit=crop",
  },
];

export function calculateAverageRating(dish: Dish): number {
  const { taste, texture, bangForBuck } = dish.ratings;
  return Number(((taste + texture + bangForBuck) / 3).toFixed(1));
}

export function getTopRatedDishes(count: number = 5): Dish[] {
  return [...dishes]
    .sort((a, b) => calculateAverageRating(b) - calculateAverageRating(a))
    .slice(0, count);
}

export function getBottomRatedDishes(count: number = 5): Dish[] {
  return [...dishes]
    .sort((a, b) => calculateAverageRating(a) - calculateAverageRating(b))
    .slice(0, count);
}
