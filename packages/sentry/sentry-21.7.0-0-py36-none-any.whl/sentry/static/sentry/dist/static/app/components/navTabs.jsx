Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var classnames_1 = tslib_1.__importDefault(require("classnames"));
function NavTabs(props) {
    var underlined = props.underlined, className = props.className, tabProps = tslib_1.__rest(props, ["underlined", "className"]);
    var mergedClassName = classnames_1.default('nav nav-tabs', className, {
        'border-bottom': underlined,
    });
    return <ul className={mergedClassName} {...tabProps}/>;
}
exports.default = NavTabs;
//# sourceMappingURL=navTabs.jsx.map