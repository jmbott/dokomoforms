import React from 'react';

/*
 * Big 'ol button
 *
 * props:
 *  @type: Type of button (class name from ratchet usually) defaults to btn-primary
 *  @buttonFunction: What to do on click events
 *  @text: Text of the button
 */
export default class {
    render() {
        var buttonClasses = 'btn btn-block navigate-right page_nav__next';
        if (this.props.type) {
            buttonClasses += ' ' + this.props.type;
        } else {
            buttonClasses += ' btn-primary';
        }

        return (
            <div className='bar-padded'>
                <button onClick={this.props.buttonFunction} className={buttonClasses}>
                    {this.props.text}
                </button>
            </div>
       );
    }
});
