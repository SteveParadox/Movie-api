import React, { Component } from "react";

// To utilize redux for the api use connect
import { connect } from "react-redux";
import { getItems } from "../actions/itemActions";
import PropTypes from "prop-types";

class SubscribeLayout extends Component {
    componentDidMount() {
        this.props.getItems();
    }

    render() {
        const { items } = this.props.item;
        return (
            <div>Hello dear</div>
        );
    }
}

SubscribeLayout.propTypes = {
    getItems: PropTypes.func.isRequired,
    sign_in: PropTypes.object.isRequired
}

const mapStateToProps = (state) => ({
    a: state.a
});

export default connect(mapStateToProps, { getItems })(SubscribeLayout);