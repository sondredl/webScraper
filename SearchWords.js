import React, {useState, useEffect } from 'react';

const SearchWordsComponent = () => {
    const [searchWords, setSearchWords] = useState([]);

    useEffect(() =>{
        fetch('/searchWords.json')
        .then((response) => response.json())
        .then((data) => setSearchWords(data))
        .then((error) => console.error('error fetching json search words', error));
    }, []);

    return (
        <div>
            <h1>
                SearchWords
            </h1>
            <ul>
                {searchWords.map((searchWords, index) => (
                    <li key={index}>{company}</li>
                ))}
            </ul>
        </div>
    );
};

export default SearchWordsComponent;