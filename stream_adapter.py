from typing import List

PAD_VALUE_MAX = 2

class StreamAdapter:
    def __init__(self, chunk_size: int):
        self.next_pad_value = 1
        self.chunk_size = chunk_size

    def get_stream_chunks(self, message: List[int]) -> List[List[int]]:
        if not message:
            return []
        
        message = self.replace_sequence(message, [5,5,5], [6,6,6])
        
        if self.next_pad_value > 1:
            message = list(range(self.next_pad_value, PAD_VALUE_MAX + 1)) + message
            self.next_pad_value = 1

        chunks = [message[i:i + self.chunk_size] for i in range(0, len(message), self.chunk_size)]

        if len(chunks[-1]) < self.chunk_size:
            chunks[-1] = self.pad_chunck(chunks[-1])

        return chunks
    
    def replace_sequence(self, nums: list[int], target: list[int], replacement: list[int]) -> list[int]:
        result = []
        i = 0
        sequence_len = len(target)

        while i < len(nums):
            if nums[i:i+sequence_len] == target:
                result.extend(replacement)
                i += sequence_len
            else:
                result.append(nums[i])
                i += 1

        return result


    def pad_chunck(self, chunk: List[int]) -> List[int]:
        amount_to_pad = self.chunk_size - len(chunk)
        result = chunk.copy()
        
        for _ in range(amount_to_pad):
            result.append(self.next_pad_value)
            self.next_pad_value = (self.next_pad_value % PAD_VALUE_MAX) + 1

        return result