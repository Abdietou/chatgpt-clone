export interface MyRequestInit extends RequestInit {
  method?: string;
  headers?: HeadersInit;
  body?: BodyInit | null;
}
