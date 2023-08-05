Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var performance_1 = require("app/actionCreators/performance");
var icons_1 = require("app/icons");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var KeyTransactionField = /** @class */ (function (_super) {
    tslib_1.__extends(KeyTransactionField, _super);
    function KeyTransactionField(props) {
        var _this = _super.call(this, props) || this;
        _this.toggleKeyTransactionHandler = function () {
            var _a = _this.props, api = _a.api, organization = _a.organization, transactionName = _a.transactionName;
            var isKeyTransaction = _this.state.isKeyTransaction;
            var projectId = _this.getProjectId();
            // All the props are guaranteed to be not undefined at this point
            // as they have all been validated in the render method.
            performance_1.toggleKeyTransaction(api, isKeyTransaction, organization.slug, [projectId], transactionName).then(function () {
                _this.setState({
                    isKeyTransaction: !isKeyTransaction,
                });
            });
        };
        _this.state = {
            isKeyTransaction: !!props.isKeyTransaction,
        };
        return _this;
    }
    KeyTransactionField.prototype.getProjectId = function () {
        var _a = this.props, projects = _a.projects, projectSlug = _a.projectSlug;
        var project = projects.find(function (proj) { return proj.slug === projectSlug; });
        if (!project) {
            return null;
        }
        return project.id;
    };
    KeyTransactionField.prototype.render = function () {
        var _a = this.props, organization = _a.organization, projectSlug = _a.projectSlug, transactionName = _a.transactionName;
        var isKeyTransaction = this.state.isKeyTransaction;
        var star = (<StyledKey color={isKeyTransaction ? 'yellow300' : 'gray200'} isSolid={isKeyTransaction} data-test-id="key-transaction-column"/>);
        // All these fields need to be defined in order to toggle a key transaction
        // Since they're not defined, we just render a plain star icon with no action
        // associated with it
        if (organization === undefined ||
            projectSlug === undefined ||
            transactionName === undefined ||
            this.getProjectId() === null) {
            return star;
        }
        return <KeyColumn onClick={this.toggleKeyTransactionHandler}>{star}</KeyColumn>;
    };
    return KeyTransactionField;
}(react_1.Component));
var KeyColumn = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject([""], [""])));
var StyledKey = styled_1.default(icons_1.IconStar)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  cursor: pointer;\n  vertical-align: middle;\n"], ["\n  cursor: pointer;\n  vertical-align: middle;\n"])));
exports.default = withApi_1.default(withProjects_1.default(KeyTransactionField));
var templateObject_1, templateObject_2;
//# sourceMappingURL=keyTransactionField.jsx.map