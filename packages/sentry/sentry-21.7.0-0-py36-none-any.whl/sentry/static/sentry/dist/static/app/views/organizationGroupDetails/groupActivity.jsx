Object.defineProperty(exports, "__esModule", { value: true });
exports.GroupActivity = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var group_1 = require("app/actionCreators/group");
var indicator_1 = require("app/actionCreators/indicator");
var author_1 = tslib_1.__importDefault(require("app/components/activity/author"));
var item_1 = tslib_1.__importDefault(require("app/components/activity/item"));
var note_1 = tslib_1.__importDefault(require("app/components/activity/note"));
var inputWithStorage_1 = tslib_1.__importDefault(require("app/components/activity/note/inputWithStorage"));
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var reprocessedBox_1 = tslib_1.__importDefault(require("app/components/reprocessedBox"));
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var types_1 = require("app/types");
var guid_1 = require("app/utils/guid");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var groupActivityItem_1 = tslib_1.__importDefault(require("./groupActivityItem"));
var utils_1 = require("./utils");
var GroupActivity = /** @class */ (function (_super) {
    tslib_1.__extends(GroupActivity, _super);
    function GroupActivity() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // TODO(dcramer): only re-render on group/activity change
        _this.state = {
            createBusy: false,
            error: false,
            errorJSON: null,
            inputId: guid_1.uniqueId(),
        };
        _this.handleNoteDelete = function (_a) {
            var modelId = _a.modelId, oldText = _a.text;
            return tslib_1.__awaiter(_this, void 0, void 0, function () {
                var _b, api, group, _err_1;
                return tslib_1.__generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            _b = this.props, api = _b.api, group = _b.group;
                            indicator_1.addLoadingMessage(locale_1.t('Removing comment...'));
                            _c.label = 1;
                        case 1:
                            _c.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, group_1.deleteNote(api, group, modelId, oldText)];
                        case 2:
                            _c.sent();
                            indicator_1.clearIndicators();
                            return [3 /*break*/, 4];
                        case 3:
                            _err_1 = _c.sent();
                            indicator_1.addErrorMessage(locale_1.t('Failed to delete comment'));
                            return [3 /*break*/, 4];
                        case 4: return [2 /*return*/];
                    }
                });
            });
        };
        /**
         * Note: This is nearly the same logic as `app/views/alerts/details/activity`
         * This can be abstracted a bit if we create more objects that can have activities
         */
        _this.handleNoteCreate = function (note) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, group, error_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, group = _a.group;
                        this.setState({
                            createBusy: true,
                        });
                        indicator_1.addLoadingMessage(locale_1.t('Posting comment...'));
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, group_1.createNote(api, group, note)];
                    case 2:
                        _b.sent();
                        this.setState({
                            createBusy: false,
                            // This is used as a `key` to Note Input so that after successful post
                            // we reset the value of the input
                            inputId: guid_1.uniqueId(),
                        });
                        indicator_1.clearIndicators();
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.setState({
                            createBusy: false,
                            error: true,
                            errorJSON: error_1.responseJSON || constants_1.DEFAULT_ERROR_JSON,
                        });
                        indicator_1.addErrorMessage(locale_1.t('Unable to post comment'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleNoteUpdate = function (note, _a) {
            var modelId = _a.modelId, oldText = _a.text;
            return tslib_1.__awaiter(_this, void 0, void 0, function () {
                var _b, api, group, error_2;
                return tslib_1.__generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            _b = this.props, api = _b.api, group = _b.group;
                            indicator_1.addLoadingMessage(locale_1.t('Updating comment...'));
                            _c.label = 1;
                        case 1:
                            _c.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, group_1.updateNote(api, group, note, modelId, oldText)];
                        case 2:
                            _c.sent();
                            indicator_1.clearIndicators();
                            return [3 /*break*/, 4];
                        case 3:
                            error_2 = _c.sent();
                            this.setState({
                                error: true,
                                errorJSON: error_2.responseJSON || constants_1.DEFAULT_ERROR_JSON,
                            });
                            indicator_1.addErrorMessage(locale_1.t('Unable to update comment'));
                            return [3 /*break*/, 4];
                        case 4: return [2 /*return*/];
                    }
                });
            });
        };
        return _this;
    }
    GroupActivity.prototype.render = function () {
        var _this = this;
        var _a = this.props, group = _a.group, organization = _a.organization;
        var activities = group.activity, count = group.count, groupId = group.id;
        var groupCount = Number(count);
        var mostRecentActivity = utils_1.getGroupMostRecentActivity(activities);
        var reprocessingStatus = utils_1.getGroupReprocessingStatus(group, mostRecentActivity);
        var me = configStore_1.default.get('user');
        var projectSlugs = group && group.project ? [group.project.slug] : [];
        var noteProps = {
            minHeight: 140,
            group: group,
            projectSlugs: projectSlugs,
            placeholder: locale_1.t('Add details or updates to this event. \nTag users with @, or teams with #'),
        };
        return (<react_1.Fragment>
        {(reprocessingStatus === utils_1.ReprocessingStatus.REPROCESSED_AND_HASNT_EVENT ||
                reprocessingStatus === utils_1.ReprocessingStatus.REPROCESSED_AND_HAS_EVENT) && (<StyledReprocessedBox reprocessActivity={mostRecentActivity} groupCount={groupCount} orgSlug={organization.slug} groupId={groupId}/>)}
        <div className="row">
          <div className="col-md-9">
            <div>
              <item_1.default author={{ type: 'user', user: me }}>
                {function () { return (<inputWithStorage_1.default key={_this.state.inputId} storageKey="groupinput:latest" itemKey={group.id} onCreate={_this.handleNoteCreate} busy={_this.state.createBusy} error={_this.state.error} errorJSON={_this.state.errorJSON} {...noteProps}/>); }}
              </item_1.default>

              {group.activity.map(function (item) {
                var _a;
                var authorName = item.user ? item.user.name : 'Sentry';
                if (item.type === types_1.GroupActivityType.NOTE) {
                    return (<errorBoundary_1.default mini key={"note-" + item.id}>
                      <note_1.default showTime={false} text={item.data.text} modelId={item.id} user={item.user} dateCreated={item.dateCreated} authorName={authorName} onDelete={_this.handleNoteDelete} onUpdate={_this.handleNoteUpdate} {...noteProps}/>
                    </errorBoundary_1.default>);
                }
                return (<errorBoundary_1.default mini key={"item-" + item.id}>
                    <item_1.default author={{
                        type: item.user ? 'user' : 'system',
                        user: (_a = item.user) !== null && _a !== void 0 ? _a : undefined,
                    }} date={item.dateCreated} header={<groupActivityItem_1.default author={<author_1.default>{authorName}</author_1.default>} activity={item} orgSlug={_this.props.params.orgId} projectId={group.project.id}/>}/>
                  </errorBoundary_1.default>);
            })}
            </div>
          </div>
        </div>
      </react_1.Fragment>);
    };
    return GroupActivity;
}(react_1.Component));
exports.GroupActivity = GroupActivity;
exports.default = withApi_1.default(withOrganization_1.default(GroupActivity));
var StyledReprocessedBox = styled_1.default(reprocessedBox_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin: -", " -", " ", " -", ";\n  z-index: 1;\n"], ["\n  margin: -", " -", " ", " -", ";\n  z-index: 1;\n"])), space_1.default(3), space_1.default(4), space_1.default(4), space_1.default(4));
var templateObject_1;
//# sourceMappingURL=groupActivity.jsx.map