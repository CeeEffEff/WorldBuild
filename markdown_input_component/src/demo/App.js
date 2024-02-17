/* eslint no-magic-numbers: 0 */
import React, { useState } from 'react';

import { MarkdownInputComponent } from '../lib';

const App = () => {

    const [state, setState] = useState({value:'Add a description...'});
    const setProps = (newProps) => {
            setState(newProps);
        };

    return (
        <div>
            <MarkdownInputComponent
                setProps={setProps}
                {...state}
            />
        </div>
    )
};


export default App;
