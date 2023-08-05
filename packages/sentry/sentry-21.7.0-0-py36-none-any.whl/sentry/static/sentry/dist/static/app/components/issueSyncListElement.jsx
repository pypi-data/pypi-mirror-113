Object.defineProperty(exports, "__esModule", { value: true });
exports.IntegrationLink = exports.IssueSyncListElementContainer = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var capitalize_1 = tslib_1.__importDefault(require("lodash/capitalize"));
var hovercard_1 = tslib_1.__importDefault(require("app/components/hovercard"));
var icons_1 = require("app/icons");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var callIfFunction_1 = require("app/utils/callIfFunction");
var integrationUtil_1 = require("app/utils/integrationUtil");
var IssueSyncListElement = /** @class */ (function (_super) {
    tslib_1.__extends(IssueSyncListElement, _super);
    function IssueSyncListElement() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.hoverCardRef = React.createRef();
        _this.handleDelete = function () {
            callIfFunction_1.callIfFunction(_this.props.onClose, _this.props.externalIssueId);
        };
        _this.handleIconClick = function () {
            if (_this.isLinked()) {
                _this.handleDelete();
            }
            else if (_this.props.onOpen) {
                _this.props.onOpen();
            }
        };
        return _this;
    }
    IssueSyncListElement.prototype.componentDidUpdate = function (nextProps) {
        if (this.props.showHoverCard !== nextProps.showHoverCard &&
            nextProps.showHoverCard === undefined) {
            this.hoverCardRef.current && this.hoverCardRef.current.handleToggleOff();
        }
    };
    IssueSyncListElement.prototype.isLinked = function () {
        return !!(this.props.externalIssueLink && this.props.externalIssueId);
    };
    IssueSyncListElement.prototype.getIcon = function () {
        return integrationUtil_1.getIntegrationIcon(this.props.integrationType);
    };
    IssueSyncListElement.prototype.getPrettyName = function () {
        var type = this.props.integrationType;
        switch (type) {
            case 'gitlab':
                return 'GitLab';
            case 'github':
                return 'GitHub';
            case 'github_enterprise':
                return 'GitHub Enterprise';
            case 'vsts':
                return 'Azure DevOps';
            case 'jira_server':
                return 'Jira Server';
            default:
                return capitalize_1.default(type);
        }
    };
    IssueSyncListElement.prototype.getLink = function () {
        return (<exports.IntegrationLink href={this.props.externalIssueLink || undefined} onClick={!this.isLinked() ? this.props.onOpen : undefined}>
        {this.getText()}
      </exports.IntegrationLink>);
    };
    IssueSyncListElement.prototype.getText = function () {
        if (this.props.children) {
            return this.props.children;
        }
        if (this.props.externalIssueDisplayName) {
            return this.props.externalIssueDisplayName;
        }
        if (this.props.externalIssueKey) {
            return this.props.externalIssueKey;
        }
        return "Link " + this.getPrettyName() + " Issue";
    };
    IssueSyncListElement.prototype.render = function () {
        var _this = this;
        return (<exports.IssueSyncListElementContainer>
        <react_1.ClassNames>
          {function (_a) {
                var css = _a.css;
                return (<hovercard_1.default ref={_this.hoverCardRef} containerClassName={css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n                display: flex;\n                align-items: center;\n                min-width: 0; /* flex-box overflow workaround */\n              "], ["\n                display: flex;\n                align-items: center;\n                min-width: 0; /* flex-box overflow workaround */\n              "])))} header={_this.props.hoverCardHeader} body={_this.props.hoverCardBody} bodyClassName="issue-list-body" show={_this.props.showHoverCard}>
              {_this.getIcon()}
              {_this.getLink()}
            </hovercard_1.default>);
            }}
        </react_1.ClassNames>
        {(this.props.onClose || this.props.onOpen) && (<StyledIcon onClick={this.handleIconClick}>
            {this.isLinked() ? <icons_1.IconClose /> : this.props.onOpen ? <icons_1.IconAdd /> : null}
          </StyledIcon>)}
      </exports.IssueSyncListElementContainer>);
    };
    return IssueSyncListElement;
}(React.Component));
exports.IssueSyncListElementContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  line-height: 0;\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n\n  &:not(:last-child) {\n    margin-bottom: ", ";\n  }\n"], ["\n  line-height: 0;\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n\n  &:not(:last-child) {\n    margin-bottom: ", ";\n  }\n"])), space_1.default(2));
exports.IntegrationLink = styled_1.default('a')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  text-decoration: none;\n  padding-bottom: ", ";\n  margin-left: ", ";\n  color: ", ";\n  border-bottom: 1px solid ", ";\n  cursor: pointer;\n  line-height: 1;\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n\n  &,\n  &:hover {\n    border-bottom: 1px solid ", ";\n  }\n"], ["\n  text-decoration: none;\n  padding-bottom: ", ";\n  margin-left: ", ";\n  color: ", ";\n  border-bottom: 1px solid ", ";\n  cursor: pointer;\n  line-height: 1;\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n\n  &,\n  &:hover {\n    border-bottom: 1px solid ", ";\n  }\n"])), space_1.default(0.25), space_1.default(1), function (p) { return p.theme.textColor; }, function (p) { return p.theme.textColor; }, function (p) { return p.theme.blue300; });
var StyledIcon = styled_1.default('span')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  cursor: pointer;\n"], ["\n  color: ", ";\n  cursor: pointer;\n"])), function (p) { return p.theme.textColor; });
exports.default = IssueSyncListElement;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=issueSyncListElement.jsx.map