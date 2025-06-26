from typing import List

PAD_VALUE_MAX = 2

class StreamAdapter:
    def __init__(self, message_size: int):
        self.next_pad_value = 1
        self.message_size = message_size

    def get_stream_chunks(self, chunk: List[int]) -> List[List[int]]:
        if not chunk:
            return []
        
        chunk = self.replace_sequence(chunk, [5,5,5], [6,6,6])
        
        if self.next_pad_value > 1:
            chunk = list(range(self.next_pad_value, PAD_VALUE_MAX + 1)) + chunk
            self.next_pad_value = 1

        messages = [chunk[i:i + self.message_size] for i in range(0, len(chunk), self.message_size)]

        if len(messages[-1]) < self.message_size:
            messages[-1] = self.pad_message(messages[-1])

        return messages
    
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


    def pad_message(self, message: List[int]) -> List[int]:
        amount_to_pad = self.message_size - len(message)
        result = message.copy()
        
        for _ in range(amount_to_pad):
            result.append(self.next_pad_value)
            self.next_pad_value = (self.next_pad_value % PAD_VALUE_MAX) + 1

        return result