Object.defineProperty(exports, "__esModule", { value: true });
exports.PluginActions = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var indicator_1 = require("app/actionCreators/indicator");
var modal_1 = require("app/actionCreators/modal");
var issueSyncListElement_1 = tslib_1.__importDefault(require("app/components/issueSyncListElement"));
var navTabs_1 = tslib_1.__importDefault(require("app/components/navTabs"));
var locale_1 = require("app/locale");
var plugins_1 = tslib_1.__importDefault(require("app/plugins"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var PluginActions = /** @class */ (function (_super) {
    tslib_1.__extends(PluginActions, _super);
    function PluginActions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            issue: null,
            pluginLoading: false,
        };
        _this.deleteIssue = function () {
            var plugin = tslib_1.__assign(tslib_1.__assign({}, _this.props.plugin), { issue: null });
            // override plugin.issue so that 'create/link' Modal
            // doesn't think the plugin still has an issue linked
            var endpoint = "/issues/" + _this.props.group.id + "/plugins/" + plugin.slug + "/unlink/";
            _this.props.api.request(endpoint, {
                success: function () {
                    _this.loadPlugin(plugin);
                    indicator_1.addSuccessMessage(locale_1.t('Successfully unlinked issue.'));
                },
                error: function () {
                    indicator_1.addErrorMessage(locale_1.t('Unable to unlink issue'));
                },
            });
        };
        _this.loadPlugin = function (data) {
            _this.setState({
                pluginLoading: true,
            }, function () {
                plugins_1.default.load(data, function () {
                    var issue = data.issue || null;
                    _this.setState({ pluginLoading: false, issue: issue });
                });
            });
        };
        _this.handleModalClose = function (data) {
            return _this.setState({
                issue: (data === null || data === void 0 ? void 0 : data.id) && (data === null || data === void 0 ? void 0 : data.link)
                    ? { issue_id: data.id, url: data.link, label: data.label }
                    : null,
            });
        };
        _this.openModal = function () {
            var issue = _this.state.issue;
            var _a = _this.props, project = _a.project, group = _a.group, organization = _a.organization;
            var plugin = tslib_1.__assign(tslib_1.__assign({}, _this.props.plugin), { issue: issue });
            modal_1.openModal(function (deps) { return (<PluginActionsModal {...deps} project={project} group={group} organization={organization} plugin={plugin} onSuccess={_this.handleModalClose}/>); }, { onClose: _this.handleModalClose });
        };
        return _this;
    }
    PluginActions.prototype.componentDidMount = function () {
        this.loadPlugin(this.props.plugin);
    };
    PluginActions.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        if (this.props.plugin.id !== nextProps.plugin.id) {
            this.loadPlugin(nextProps.plugin);
        }
    };
    PluginActions.prototype.render = function () {
        var issue = this.state.issue;
        var plugin = tslib_1.__assign(tslib_1.__assign({}, this.props.plugin), { issue: issue });
        return (<issueSyncListElement_1.default onOpen={this.openModal} externalIssueDisplayName={issue ? issue.label : null} externalIssueId={issue ? issue.issue_id : null} externalIssueLink={issue ? issue.url : null} onClose={this.deleteIssue} integrationType={plugin.id}/>);
    };
    return PluginActions;
}(react_1.Component));
exports.PluginActions = PluginActions;
var PluginActionsModal = /** @class */ (function (_super) {
    tslib_1.__extends(PluginActionsModal, _super);
    function PluginActionsModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            actionType: 'create',
        };
        return _this;
    }
    PluginActionsModal.prototype.render = function () {
        var _this = this;
        var _a = this.props, Header = _a.Header, Body = _a.Body, group = _a.group, project = _a.project, organization = _a.organization, plugin = _a.plugin, onSuccess = _a.onSuccess;
        var actionType = this.state.actionType;
        return (<react_1.Fragment>
        <Header closeButton>
          {locale_1.tct('[name] Issue', { name: plugin.name || plugin.title })}
        </Header>
        <navTabs_1.default underlined>
          <li className={actionType === 'create' ? 'active' : ''}>
            <a onClick={function () { return _this.setState({ actionType: 'create' }); }}>{locale_1.t('Create')}</a>
          </li>
          <li className={actionType === 'link' ? 'active' : ''}>
            <a onClick={function () { return _this.setState({ actionType: 'link' }); }}>{locale_1.t('Link')}</a>
          </li>
        </navTabs_1.default>
        {actionType && (
            // need the key here so React will re-render
            // with new action prop
            <Body key={actionType}>
            {plugins_1.default.get(plugin).renderGroupActions({
                    plugin: plugin,
                    group: group,
                    project: project,
                    organization: organization,
                    actionType: actionType,
                    onSuccess: onSuccess,
                })}
          </Body>)}
      </react_1.Fragment>);
    };
    return PluginActionsModal;
}(react_1.Component));
exports.default = withApi_1.default(withOrganization_1.default(PluginActions));
//# sourceMappingURL=pluginActions.jsx.map