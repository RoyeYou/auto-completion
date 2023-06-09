import streamlit as st
import pickle


class TrieNode:
    def __init__(self):
        self.children = {}  # store 'children' of the node, key as characters
        self.end_of_word = False  # record whether the word ends
        self.frequency = 0  # store frequency


class Trie:
    def __init__(self):
        self.root = TrieNode()  # TrieNode object as the root

    def insert(self, word):
        node = self.root
        for char in word:  # add characters of the word into node's children
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.end_of_word = True
        node.frequency += 1  # Increase frequency of the inserted word

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.end_of_word

    def suggestion(self, prefix):
        node = self.root
        for char in prefix:  # check each character whether it's a child node for the current character
            if char not in node.children:
                return []
            node = node.children[char]
        return [result[0] for result in self._dfs(node, prefix)]

    def _dfs(self, node, prefix):  # DFS depth-first search starting from prefix
        results = []
        if node.end_of_word:  # if the query is already an 'end' word
            results.append((prefix, node.frequency))
        for char, child_node in node.children.items():
            results.extend(self._dfs(child_node, prefix + char))  # extend result based on child node and updated prefix
        t = sorted(results, key=lambda x: x[1], reverse=True)
        return t[0:5]


@st.cache_resource
def load_model(model_path):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model


model_path = 'trie.pkl'
trie = load_model(model_path)


def main():
    st.title("Welcome to VeePee")
    user_input = st.text_input("Start typing here...")

    if user_input:
        results = trie.suggestion(user_input.lower())
        for result in results:
            st.write(result)


if __name__ == "__main__":
    main()
