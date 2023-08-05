Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var groupBy_1 = tslib_1.__importDefault(require("lodash/groupBy"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var item_1 = tslib_1.__importDefault(require("app/components/activity/item"));
var note_1 = tslib_1.__importDefault(require("app/components/activity/note"));
var inputWithStorage_1 = tslib_1.__importDefault(require("app/components/activity/note/inputWithStorage"));
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var types_1 = require("../../types");
var activityPlaceholder_1 = tslib_1.__importDefault(require("./activityPlaceholder"));
var dateDivider_1 = tslib_1.__importDefault(require("./dateDivider"));
var statusItem_1 = tslib_1.__importDefault(require("./statusItem"));
/**
 * Activity component on Incident Details view
 * Allows user to leave a comment on an alertId as well as
 * fetch and render existing activity items.
 */
var Activity = /** @class */ (function (_super) {
    tslib_1.__extends(Activity, _super);
    function Activity() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleUpdateNote = function (note, _a) {
            var activity = _a.activity;
            var onUpdateNote = _this.props.onUpdateNote;
            onUpdateNote(note, activity);
        };
        _this.handleDeleteNote = function (_a) {
            var activity = _a.activity;
            var onDeleteNote = _this.props.onDeleteNote;
            onDeleteNote(activity);
        };
        return _this;
    }
    Activity.prototype.render = function () {
        var _this = this;
        var _a = this.props, loading = _a.loading, error = _a.error, me = _a.me, alertId = _a.alertId, incident = _a.incident, activities = _a.activities, noteInputId = _a.noteInputId, createBusy = _a.createBusy, createError = _a.createError, createErrorJSON = _a.createErrorJSON, onCreateNote = _a.onCreateNote;
        var noteProps = tslib_1.__assign({ minHeight: 80, projectSlugs: (incident && incident.projects) || [] }, this.props.noteInputProps);
        var activitiesByDate = groupBy_1.default(activities, function (_a) {
            var dateCreated = _a.dateCreated;
            return moment_1.default(dateCreated).format('ll');
        });
        var today = moment_1.default().format('ll');
        return (<div>
        <item_1.default author={{ type: 'user', user: me }}>
          {function () { return (<inputWithStorage_1.default key={noteInputId} storageKey="incidentIdinput" itemKey={alertId} onCreate={onCreateNote} busy={createBusy} error={createError} errorJSON={createErrorJSON} placeholder={locale_1.t('Leave a comment, paste a tweet, or link any other relevant information about this alert...')} {...noteProps}/>); }}
        </item_1.default>

        {error && <loadingError_1.default message={locale_1.t('There was a problem loading activities')}/>}

        {loading && (<React.Fragment>
            <activityPlaceholder_1.default />
            <activityPlaceholder_1.default />
            <activityPlaceholder_1.default />
          </React.Fragment>)}

        {!loading &&
                !error &&
                Object.entries(activitiesByDate).map(function (_a) {
                    var _b = tslib_1.__read(_a, 2), date = _b[0], activitiesForDate = _b[1];
                    var title = date === today ? (locale_1.t('Today')) : (<React.Fragment>
                  {date} <StyledTimeSince date={date}/>
                </React.Fragment>);
                    return (<React.Fragment key={date}>
                <dateDivider_1.default>{title}</dateDivider_1.default>
                {activitiesForDate &&
                            activitiesForDate.map(function (activity) {
                                var _a, _b;
                                var authorName = (_b = (_a = activity.user) === null || _a === void 0 ? void 0 : _a.name) !== null && _b !== void 0 ? _b : 'Sentry';
                                if (activity.type === types_1.IncidentActivityType.COMMENT) {
                                    return (<errorBoundary_1.default mini key={"note-" + activity.id}>
                          <note_1.default showTime user={activity.user} modelId={activity.id} text={activity.comment || ''} dateCreated={activity.dateCreated} activity={activity} authorName={authorName} onDelete={_this.handleDeleteNote} onUpdate={_this.handleUpdateNote} {...noteProps}/>
                        </errorBoundary_1.default>);
                                }
                                else {
                                    return (<errorBoundary_1.default mini key={"note-" + activity.id}>
                          <statusItem_1.default showTime incident={incident} authorName={authorName} activity={activity}/>
                        </errorBoundary_1.default>);
                                }
                            })}
              </React.Fragment>);
                })}
      </div>);
    };
    return Activity;
}(React.Component));
exports.default = Activity;
var StyledTimeSince = styled_1.default(timeSince_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  margin-left: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n  margin-left: ", ";\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeSmall; }, space_1.default(0.5));
var templateObject_1;
//# sourceMappingURL=activity.jsx.map