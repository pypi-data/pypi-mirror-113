Object.defineProperty(exports, "__esModule", { value: true });
exports.ProjectProcessingIssues = exports.projectProcessingIssuesMessages = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var alertLink_1 = tslib_1.__importDefault(require("app/components/alertLink"));
var autoSelectText_1 = tslib_1.__importDefault(require("app/components/autoSelectText"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var panels_1 = require("app/components/panels");
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var processingIssues_1 = tslib_1.__importDefault(require("app/data/forms/processingIssues"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var input_1 = require("app/styles/input");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
exports.projectProcessingIssuesMessages = {
    native_no_crashed_thread: locale_1.t('No crashed thread found in crash report'),
    native_internal_failure: locale_1.t('Internal failure when attempting to symbolicate: {error}'),
    native_bad_dsym: locale_1.t('The debug information file used was broken.'),
    native_missing_optionally_bundled_dsym: locale_1.t('An optional debug information file was missing.'),
    native_missing_dsym: locale_1.t('A required debug information file was missing.'),
    native_missing_system_dsym: locale_1.t('A system debug information file was missing.'),
    native_missing_symbol: locale_1.t('Could not resolve one or more frames in debug information file.'),
    native_simulator_frame: locale_1.t('Encountered an unprocessable simulator frame.'),
    native_unknown_image: locale_1.t('A binary image is referenced that is unknown.'),
    proguard_missing_mapping: locale_1.t('A proguard mapping file was missing.'),
    proguard_missing_lineno: locale_1.t('A proguard mapping file does not contain line info.'),
};
var HELP_LINKS = {
    native_missing_dsym: 'https://docs.sentry.io/platforms/apple/dsym/',
    native_bad_dsym: 'https://docs.sentry.io/platforms/apple/dsym/',
    native_missing_system_dsym: 'https://develop.sentry.dev/self-hosted/',
    native_missing_symbol: 'https://develop.sentry.dev/self-hosted/',
};
var ProjectProcessingIssues = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectProcessingIssues, _super);
    function ProjectProcessingIssues() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            formData: {},
            loading: true,
            reprocessing: false,
            expected: 0,
            error: false,
            processingIssues: null,
            pageLinks: null,
        };
        _this.fetchData = function () {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            _this.setState({
                expected: _this.state.expected + 2,
            });
            _this.props.api.request("/projects/" + orgId + "/" + projectId + "/", {
                success: function (data) {
                    var expected = _this.state.expected - 1;
                    _this.setState({
                        expected: expected,
                        loading: expected > 0,
                        formData: data.options,
                    });
                },
                error: function () {
                    var expected = _this.state.expected - 1;
                    _this.setState({
                        expected: expected,
                        error: true,
                        loading: expected > 0,
                    });
                },
            });
            _this.props.api.request("/projects/" + orgId + "/" + projectId + "/processingissues/?detailed=1", {
                success: function (data, _, jqXHR) {
                    var _a;
                    var expected = _this.state.expected - 1;
                    _this.setState({
                        expected: expected,
                        error: false,
                        loading: expected > 0,
                        processingIssues: data,
                        pageLinks: (_a = jqXHR === null || jqXHR === void 0 ? void 0 : jqXHR.getResponseHeader('Link')) !== null && _a !== void 0 ? _a : null,
                    });
                },
                error: function () {
                    var expected = _this.state.expected - 1;
                    _this.setState({
                        expected: expected,
                        error: true,
                        loading: expected > 0,
                    });
                },
            });
        };
        _this.sendReprocessing = function (e) {
            e.preventDefault();
            _this.setState({
                loading: true,
                reprocessing: true,
            });
            indicator_1.addLoadingMessage(locale_1.t('Started reprocessing\u2026'));
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            _this.props.api.request("/projects/" + orgId + "/" + projectId + "/reprocessing/", {
                method: 'POST',
                success: function () {
                    _this.fetchData();
                    _this.setState({
                        reprocessing: false,
                    });
                },
                error: function () {
                    _this.setState({
                        reprocessing: false,
                    });
                },
                complete: function () {
                    indicator_1.clearIndicators();
                },
            });
        };
        _this.discardEvents = function () {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            _this.setState({
                expected: _this.state.expected + 1,
            });
            _this.props.api.request("/projects/" + orgId + "/" + projectId + "/processingissues/discard/", {
                method: 'DELETE',
                success: function () {
                    var expected = _this.state.expected - 1;
                    _this.setState({
                        expected: expected,
                        error: false,
                        loading: expected > 0,
                    });
                    // TODO (billyvg): Need to fix this
                    // we reload to get rid of the badge in the sidebar
                    window.location.reload();
                },
                error: function () {
                    var expected = _this.state.expected - 1;
                    _this.setState({
                        expected: expected,
                        error: true,
                        loading: expected > 0,
                    });
                },
            });
        };
        _this.deleteProcessingIssues = function () {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            _this.setState({
                expected: _this.state.expected + 1,
            });
            _this.props.api.request("/projects/" + orgId + "/" + projectId + "/processingissues/", {
                method: 'DELETE',
                success: function () {
                    var expected = _this.state.expected - 1;
                    _this.setState({
                        expected: expected,
                        error: false,
                        loading: expected > 0,
                    });
                    // TODO (billyvg): Need to fix this
                    // we reload to get rid of the badge in the sidebar
                    window.location.reload();
                },
                error: function () {
                    var expected = _this.state.expected - 1;
                    _this.setState({
                        expected: expected,
                        error: true,
                        loading: expected > 0,
                    });
                },
            });
        };
        return _this;
    }
    ProjectProcessingIssues.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ProjectProcessingIssues.prototype.renderDebugTable = function () {
        var body;
        var _a = this.state, loading = _a.loading, error = _a.error, processingIssues = _a.processingIssues;
        if (loading) {
            body = this.renderLoading();
        }
        else if (error) {
            body = <loadingError_1.default onRetry={this.fetchData}/>;
        }
        else if ((processingIssues === null || processingIssues === void 0 ? void 0 : processingIssues.hasIssues) ||
            (processingIssues === null || processingIssues === void 0 ? void 0 : processingIssues.resolveableIssues) ||
            (processingIssues === null || processingIssues === void 0 ? void 0 : processingIssues.issuesProcessing)) {
            body = this.renderResults();
        }
        else {
            body = this.renderEmpty();
        }
        return body;
    };
    ProjectProcessingIssues.prototype.renderLoading = function () {
        return (<panels_1.Panel>
        <loadingIndicator_1.default />
      </panels_1.Panel>);
    };
    ProjectProcessingIssues.prototype.renderEmpty = function () {
        return (<panels_1.Panel>
        <emptyStateWarning_1.default>
          <p>{locale_1.t('Good news! There are no processing issues.')}</p>
        </emptyStateWarning_1.default>
      </panels_1.Panel>);
    };
    ProjectProcessingIssues.prototype.getProblemDescription = function (item) {
        var msg = exports.projectProcessingIssuesMessages[item.type];
        return msg || locale_1.t('Unknown Error');
    };
    ProjectProcessingIssues.prototype.getImageName = function (path) {
        var pathSegments = path.split(/^([a-z]:\\|\\\\)/i.test(path) ? '\\' : '/');
        return pathSegments[pathSegments.length - 1];
    };
    ProjectProcessingIssues.prototype.renderProblem = function (item) {
        var description = this.getProblemDescription(item);
        var helpLink = HELP_LINKS[item.type];
        return (<div>
        <span>{description}</span>{' '}
        {helpLink && (<externalLink_1.default href={helpLink}>
            <icons_1.IconQuestion size="xs"/>
          </externalLink_1.default>)}
      </div>);
    };
    ProjectProcessingIssues.prototype.renderDetails = function (item) {
        var dsymUUID = null;
        var dsymName = null;
        var dsymArch = null;
        if (item.data._scope === 'native') {
            if (item.data.image_uuid) {
                dsymUUID = <code className="uuid">{item.data.image_uuid}</code>;
            }
            if (item.data.image_path) {
                dsymName = <em>{this.getImageName(item.data.image_path)}</em>;
            }
            if (item.data.image_arch) {
                dsymArch = item.data.image_arch;
            }
        }
        return (<span>
        {dsymUUID && <span> {dsymUUID}</span>}
        {dsymArch && <span> {dsymArch}</span>}
        {dsymName && <span> (for {dsymName})</span>}
      </span>);
    };
    ProjectProcessingIssues.prototype.renderResolveButton = function () {
        var issues = this.state.processingIssues;
        if (issues === null || this.state.reprocessing) {
            return null;
        }
        if (issues.resolveableIssues <= 0) {
            return null;
        }
        var fixButton = locale_1.tn('Click here to trigger processing for %s pending event', 'Click here to trigger processing for %s pending events', issues.resolveableIssues);
        return (<alertLink_1.default priority="info" onClick={this.sendReprocessing}>
        {locale_1.t('Pro Tip')}: {fixButton}
      </alertLink_1.default>);
    };
    ProjectProcessingIssues.prototype.renderResults = function () {
        var _this = this;
        var _a;
        var processingIssues = this.state.processingIssues;
        var fixLink = processingIssues ? processingIssues.signedLink : false;
        var fixLinkBlock = null;
        if (fixLink) {
            fixLinkBlock = (<panels_1.Panel>
          <panels_1.PanelHeader>
            {locale_1.t('Having trouble uploading debug informations? We can help!')}
          </panels_1.PanelHeader>
          <panels_1.PanelBody withPadding>
            <label>
              {locale_1.t("Paste this command into your shell and we'll attempt to upload the missing symbols from your machine:")}
            </label>
            <AutoSelectTextInput readOnly>
              curl -sL "{fixLink}" | bash
            </AutoSelectTextInput>
          </panels_1.PanelBody>
        </panels_1.Panel>);
        }
        var processingRow = null;
        if (processingIssues && processingIssues.issuesProcessing > 0) {
            processingRow = (<StyledPanelAlert type="info" icon={<icons_1.IconSettings size="sm"/>}>
          {locale_1.tn('Reprocessing %s event …', 'Reprocessing %s events …', processingIssues.issuesProcessing)}
        </StyledPanelAlert>);
        }
        return (<React.Fragment>
        {fixLinkBlock}
        <h3>
          {locale_1.t('Pending Issues')}
          <access_1.default access={['project:write']}>
            {function (_a) {
                var hasAccess = _a.hasAccess;
                return (<button_1.default size="small" className="pull-right" disabled={!hasAccess} onClick={function () { return _this.discardEvents(); }}>
                {locale_1.t('Discard all')}
              </button_1.default>);
            }}
          </access_1.default>
        </h3>
        <panels_1.PanelTable headers={[locale_1.t('Problem'), locale_1.t('Details'), locale_1.t('Events'), locale_1.t('Last seen')]}>
          {processingRow}
          {(_a = processingIssues === null || processingIssues === void 0 ? void 0 : processingIssues.issues) === null || _a === void 0 ? void 0 : _a.map(function (item, idx) { return (<React.Fragment key={idx}>
              <div>{_this.renderProblem(item)}</div>
              <div>{_this.renderDetails(item)}</div>
              <div>{item.numEvents + ''}</div>
              <div>
                <timeSince_1.default date={item.lastSeen}/>
              </div>
            </React.Fragment>); })}
        </panels_1.PanelTable>
      </React.Fragment>);
    };
    ProjectProcessingIssues.prototype.renderReprocessingSettings = function () {
        var access = new Set(this.props.organization.access);
        if (this.state.loading) {
            return this.renderLoading();
        }
        var formData = this.state.formData;
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return (<form_1.default saveOnBlur onSubmitSuccess={this.deleteProcessingIssues} apiEndpoint={"/projects/" + orgId + "/" + projectId + "/"} apiMethod="PUT" initialData={formData}>
        <jsonForm_1.default access={access} forms={processingIssues_1.default} renderHeader={function () { return (<panels_1.PanelAlert type="warning">
              <textBlock_1.default noMargin>
                {locale_1.t("Reprocessing does not apply to Minidumps. Even when enabled,\n                    Minidump events with processing issues will show up in the\n                    issues stream immediately and cannot be reprocessed.")}
              </textBlock_1.default>
            </panels_1.PanelAlert>); }}/>
      </form_1.default>);
    };
    ProjectProcessingIssues.prototype.render = function () {
        var projectId = this.props.params.projectId;
        var title = locale_1.t('Processing Issues');
        return (<div>
        <sentryDocumentTitle_1.default title={title} projectSlug={projectId}/>
        <settingsPageHeader_1.default title={title}/>
        <textBlock_1.default>
          {locale_1.t("For some platforms the event processing requires configuration or\n          manual action.  If a misconfiguration happens or some necessary\n          steps are skipped, issues can occur during processing. (The most common\n          reason for this is missing debug symbols.) In these cases you can see\n          all the problems here with guides of how to correct them.")}
        </textBlock_1.default>
        {this.renderDebugTable()}
        {this.renderResolveButton()}
        {this.renderReprocessingSettings()}
      </div>);
    };
    return ProjectProcessingIssues;
}(React.Component));
exports.ProjectProcessingIssues = ProjectProcessingIssues;
var StyledPanelAlert = styled_1.default(panels_1.PanelAlert)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  grid-column: 1/5;\n"], ["\n  grid-column: 1/5;\n"])));
var AutoSelectTextInput = styled_1.default(autoSelectText_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-family: ", ";\n  ", ";\n"], ["\n  font-family: ", ";\n  ", ";\n"])), function (p) { return p.theme.text.familyMono; }, function (p) { return input_1.inputStyles(p); });
exports.default = withApi_1.default(withOrganization_1.default(ProjectProcessingIssues));
var templateObject_1, templateObject_2;
//# sourceMappingURL=projectProcessingIssues.jsx.map