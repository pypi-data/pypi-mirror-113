Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var isObject_1 = tslib_1.__importDefault(require("lodash/isObject"));
var keyBy_1 = tslib_1.__importDefault(require("lodash/keyBy"));
var pickBy_1 = tslib_1.__importDefault(require("lodash/pickBy"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var externalIssuesList_1 = tslib_1.__importDefault(require("app/components/group/externalIssuesList"));
var participants_1 = tslib_1.__importDefault(require("app/components/group/participants"));
var releaseStats_1 = tslib_1.__importDefault(require("app/components/group/releaseStats"));
var suggestedOwners_1 = tslib_1.__importDefault(require("app/components/group/suggestedOwners/suggestedOwners"));
var tagDistributionMeter_1 = tslib_1.__importDefault(require("app/components/group/tagDistributionMeter"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var sidebarSection_1 = tslib_1.__importDefault(require("./sidebarSection"));
var GroupSidebar = /** @class */ (function (_super) {
    tslib_1.__extends(GroupSidebar, _super);
    function GroupSidebar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            participants: [],
            environments: _this.props.environments,
        };
        return _this;
    }
    GroupSidebar.prototype.componentDidMount = function () {
        this.fetchAllEnvironmentsGroupData();
        this.fetchCurrentRelease();
        this.fetchParticipants();
        this.fetchTagData();
    };
    GroupSidebar.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        if (!isEqual_1.default(nextProps.environments, this.props.environments)) {
            this.setState({ environments: nextProps.environments }, this.fetchTagData);
        }
    };
    GroupSidebar.prototype.fetchAllEnvironmentsGroupData = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, group, api, query, allEnvironmentsGroupData, _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, group = _a.group, api = _a.api;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        query = { collapse: 'release' };
                        return [4 /*yield*/, api.requestPromise("/issues/" + group.id + "/", {
                                query: query,
                            })];
                    case 2:
                        allEnvironmentsGroupData = _c.sent();
                        // eslint-disable-next-line react/no-did-mount-set-state
                        this.setState({ allEnvironmentsGroupData: allEnvironmentsGroupData });
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        // eslint-disable-next-line react/no-did-mount-set-state
                        this.setState({ error: true });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    GroupSidebar.prototype.fetchCurrentRelease = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, group, api, currentRelease, _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, group = _a.group, api = _a.api;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/issues/" + group.id + "/current-release/")];
                    case 2:
                        currentRelease = _c.sent();
                        this.setState({ currentRelease: currentRelease });
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        this.setState({ error: true });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    GroupSidebar.prototype.fetchParticipants = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, group, api, participants, _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, group = _a.group, api = _a.api;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/issues/" + group.id + "/participants/")];
                    case 2:
                        participants = _c.sent();
                        this.setState({
                            participants: participants,
                            error: false,
                        });
                        return [2 /*return*/, participants];
                    case 3:
                        _b = _c.sent();
                        this.setState({
                            error: true,
                        });
                        return [2 /*return*/, []];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    GroupSidebar.prototype.fetchTagData = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, group, data, _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, group = _a.group;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/issues/" + group.id + "/tags/", {
                                query: pickBy_1.default({
                                    key: group.tags.map(function (tag) { return tag.key; }),
                                    environment: this.state.environments.map(function (env) { return env.name; }),
                                }),
                            })];
                    case 2:
                        data = _c.sent();
                        this.setState({ tagsWithTopValues: keyBy_1.default(data, 'key') });
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        this.setState({
                            tagsWithTopValues: {},
                            error: true,
                        });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    GroupSidebar.prototype.renderPluginIssue = function () {
        var issues = [];
        (this.props.group.pluginIssues || []).forEach(function (plugin) {
            var issue = plugin.issue;
            // # TODO(dcramer): remove plugin.title check in Sentry 8.22+
            if (issue) {
                issues.push(<React.Fragment key={plugin.slug}>
            <span>{(plugin.shortName || plugin.name || plugin.title) + ": "}</span>
            <a href={issue.url}>{isObject_1.default(issue.label) ? issue.label.id : issue.label}</a>
          </React.Fragment>);
            }
        });
        if (!issues.length) {
            return null;
        }
        return (<sidebarSection_1.default title={locale_1.t('External Issues')}>
        <ExternalIssues>{issues}</ExternalIssues>
      </sidebarSection_1.default>);
    };
    GroupSidebar.prototype.renderParticipantData = function () {
        var _a = this.state, error = _a.error, _b = _a.participants, participants = _b === void 0 ? [] : _b;
        if (error) {
            return (<loadingError_1.default message={locale_1.t('There was an error while trying to load participants.')}/>);
        }
        return participants.length !== 0 && <participants_1.default participants={participants}/>;
    };
    GroupSidebar.prototype.render = function () {
        var _a = this.props, className = _a.className, event = _a.event, group = _a.group, organization = _a.organization, project = _a.project, environments = _a.environments;
        var _b = this.state, allEnvironmentsGroupData = _b.allEnvironmentsGroupData, currentRelease = _b.currentRelease, tagsWithTopValues = _b.tagsWithTopValues;
        var projectId = project.slug;
        return (<div className={className}>
        {event && <suggestedOwners_1.default project={project} group={group} event={event}/>}

        <releaseStats_1.default organization={organization} project={project} environments={environments} allEnvironments={allEnvironmentsGroupData} group={group} currentRelease={currentRelease}/>

        {event && (<errorBoundary_1.default mini>
            <externalIssuesList_1.default project={project} group={group} event={event}/>
          </errorBoundary_1.default>)}

        {this.renderPluginIssue()}

        <sidebarSection_1.default title={<guideAnchor_1.default target="tags" position="bottom">
              {locale_1.t('Tags')}
            </guideAnchor_1.default>}>
          {!tagsWithTopValues ? (<TagPlaceholders>
              <placeholder_1.default height="40px"/>
              <placeholder_1.default height="40px"/>
              <placeholder_1.default height="40px"/>
              <placeholder_1.default height="40px"/>
            </TagPlaceholders>) : (group.tags.map(function (tag) {
                var tagWithTopValues = tagsWithTopValues[tag.key];
                var topValues = tagWithTopValues ? tagWithTopValues.topValues : [];
                var topValuesTotal = tagWithTopValues ? tagWithTopValues.totalValues : 0;
                return (<tagDistributionMeter_1.default key={tag.key} tag={tag.key} totalValues={topValuesTotal} topValues={topValues} name={tag.name} organization={organization} projectId={projectId} group={group}/>);
            }))}
          {group.tags.length === 0 && (<p data-test-id="no-tags">
              {environments.length
                    ? locale_1.t('No tags found in the selected environments')
                    : locale_1.t('No tags found')}
            </p>)}
        </sidebarSection_1.default>

        {this.renderParticipantData()}
      </div>);
    };
    return GroupSidebar;
}(React.Component));
var TagPlaceholders = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  gap: ", ";\n  grid-auto-flow: row;\n"], ["\n  display: grid;\n  gap: ", ";\n  grid-auto-flow: row;\n"])), space_1.default(1));
var StyledGroupSidebar = styled_1.default(GroupSidebar)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var ExternalIssues = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto max-content;\n  gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: auto max-content;\n  gap: ", ";\n"])), space_1.default(2));
exports.default = withApi_1.default(StyledGroupSidebar);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=sidebar.jsx.map