export interface Product {
    id: string;
    type: string;
    name: string;
    promotion: string;
    units: number;
    post_discount_price: any[];
}

export interface Cart {
products: Product[];
}