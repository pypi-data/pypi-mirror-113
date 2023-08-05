Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var item_1 = tslib_1.__importDefault(require("app/components/activity/item"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
exports.default = react_1.withTheme(function ActivityPlaceholder(props) {
    return (<item_1.default bubbleProps={{
            backgroundColor: props.theme.backgroundSecondary,
            borderColor: props.theme.backgroundSecondary,
        }}>
      {function () { return <Placeholder />; }}
    </item_1.default>);
});
var Placeholder = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space_1.default(4));
var templateObject_1;
//# sourceMappingURL=activityPlaceholder.jsx.map