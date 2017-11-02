import React from 'react';
import ReactDOM from 'react-dom';
import ReactTestUtils from 'react-dom/test-utils';

// a noop function useful for passing into components that require it.
var noop = () => {};

describe('DontKnow', () => {
    var DontKnow;

    beforeEach(function() {
        jest.dontMock('../DontKnow.js');
        DontKnow = require('../DontKnow');
    });

    it('calls the checkBoxFunction property when pressed', () => {
        var callback = jest.genMockFunction();

        // Render a DontKnow in the document
        var dontKnow = ReactTestUtils.renderIntoDocument(
            <DontKnow checkBoxFunction={callback} />
        );

        // Simulate click on button
        ReactTestUtils.Simulate.click(
            ReactTestUtils.findRenderedDOMComponentWithTag(dontKnow, 'input')
        );

        // Verify that the callback was called once.
        expect(callback.mock.calls.length).toEqual(1);
    });

    it('is not checked by default', () => {
        // Render a DontKnow in the document
        var dontKnow = ReactTestUtils.renderIntoDocument(
            <DontKnow checkBoxFunction={noop} />
        );

        // Get the rendered element
        var dontKnowNode = ReactTestUtils.findRenderedDOMComponentWithTag(dontKnow, 'input');

        expect(dontKnowNode.defaultChecked).toEqual(false);
    });

    it('is checked by default when checked property is present', () => {
        // Render a DontKnow in the document
        var dontKnow = ReactTestUtils.renderIntoDocument(
            <DontKnow checkBoxFunction={noop} checked={true} />
        );

        // Get the rendered element
        var dontKnowNode = ReactTestUtils.findRenderedDOMComponentWithTag(dontKnow, 'input');

        expect(dontKnowNode.defaultChecked).toEqual(true);
    });
});
