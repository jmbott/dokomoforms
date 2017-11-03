var React = require('react'),
    createReactClass = require('create-react-class'),
    PropTypes = require('prop-types');

/*
 * Don't know component
 *
 * props:
 *  @checkBoxFunction: What to do on click event
 */
module.exports = createReactClass({
    render: function() {
        return (
            <div className='question__btn__other'>
                <input
                    onClick={this.props.checkBoxFunction}
                    type='checkbox'
                    id='dont-know'
                    name='dont-know'
                    defaultChecked={this.props.checked}
                />
                <label htmlFor='dont-know'>I don't know the answer</label>
            </div>
        );
    }
});
