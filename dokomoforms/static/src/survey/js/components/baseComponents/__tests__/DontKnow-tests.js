import 'raf/polyfill';
import React from 'react';
import ReactDOM from 'react-dom';
import TestUtils from 'react-dom/test-utils';
import PropTypes from 'prop-types';

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
        var dontKnow = TestUtils.renderIntoDocument(
            <DontKnow checkBoxFunction={callback} />
        );

        // Simulate click on button
        TestUtils.Simulate.click(
            TestUtils.findRenderedDOMComponentWithTag(dontKnow, 'input')
        );

        // Verify that the callback was called once.
        expect(callback.mock.calls.length).toEqual(1);
    });

    it('is not checked by default', () => {
        // Render a DontKnow in the document
        var dontKnow = TestUtils.renderIntoDocument(
            <DontKnow checkBoxFunction={noop} />
        );

        // Get the rendered element
        var dontKnowNode = TestUtils.findRenderedDOMComponentWithTag(dontKnow, 'input');

        expect(dontKnowNode.defaultChecked).toEqual(false);
    });

    it('is checked by default when checked property is present', () => {
        // Render a DontKnow in the document
        var dontKnow = TestUtils.renderIntoDocument(
            <DontKnow checked={true} checkBoxFunction={noop} />
        );

        // Get the rendered element
        var dontKnowNode = TestUtils.findRenderedDOMComponentWithTag(dontKnow, 'input');

        expect(dontKnowNode.defaultChecked).toEqual(true);
    });
});
