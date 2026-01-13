import { create } from 'zustand'

interface counterType {
  counter: number
  increaseCounter: () => void
  decreaseCounter: () => void
}
export const useCounterStore = create<counterType>((set) => ({
  counter: 0,
  increaseCounter: () => set((state) => ({ counter: state.counter + 1 })),
  decreaseCounter: () => set((state) => ({ counter: state.counter -1 }))
}))
