Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var getBadge_1 = tslib_1.__importDefault(require("./getBadge"));
/**
 * Public interface for all "id badges":
 * Organization, project, team, user
 */
var IdBadge = function (props) {
    var componentBadge = getBadge_1.default(props);
    if (!componentBadge) {
        throw new Error('IdBadge: required property missing (organization, project, team, member, user) or misconfigured');
    }
    return <InlineErrorBoundary mini>{componentBadge}</InlineErrorBoundary>;
};
exports.default = IdBadge;
var InlineErrorBoundary = styled_1.default(errorBoundary_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  background-color: transparent;\n  border-color: transparent;\n  display: flex;\n  align-items: center;\n  margin-bottom: 0;\n  box-shadow: none;\n  padding: 0; /* Because badges dont have any padding, so this should make the boundary fit well */\n"], ["\n  background-color: transparent;\n  border-color: transparent;\n  display: flex;\n  align-items: center;\n  margin-bottom: 0;\n  box-shadow: none;\n  padding: 0; /* Because badges dont have any padding, so this should make the boundary fit well */\n"])));
var templateObject_1;
//# sourceMappingURL=index.jsx.map