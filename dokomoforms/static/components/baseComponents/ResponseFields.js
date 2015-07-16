var React = require('react');
var ResponseField = require('./ResponseField.js');

module.exports = React.createClass({
    render: function() {
        var children = Array.apply(null, {length: this.props.childCount})
        var self = this;
        return (
                <div>
                {children.map(function(child, idx) {
                    return (
                            <ResponseField 
                                buttonFunction={self.props.buttonFunction}
                                type={self.props.type}
                                key={idx + 1} 
                                showMinus={self.props.childCount > 1}
                            />
                           )
                })}
                </div>
               )
    }
});
