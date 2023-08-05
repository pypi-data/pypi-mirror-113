Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var incident_1 = require("app/actionCreators/incident");
var constants_1 = require("app/constants");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var guid_1 = require("app/utils/guid");
var replaceAtArrayIndex_1 = require("app/utils/replaceAtArrayIndex");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var types_1 = require("../../types");
var activity_1 = tslib_1.__importDefault(require("./activity"));
/**
 * Activity component on Incident Details view
 * Allows user to leave a comment on an alertId as well as
 * fetch and render existing activity items.
 */
var ActivityContainer = /** @class */ (function (_super) {
    tslib_1.__extends(ActivityContainer, _super);
    function ActivityContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            error: false,
            noteInputId: guid_1.uniqueId(),
            noteInputText: '',
            createBusy: false,
            createError: false,
            createErrorJSON: null,
            activities: null,
        };
        _this.handleCreateNote = function (note) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, params, alertId, orgId, newActivity, newNote_1, error_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, params = _a.params;
                        alertId = params.alertId, orgId = params.orgId;
                        newActivity = {
                            comment: note.text,
                            type: types_1.IncidentActivityType.COMMENT,
                            dateCreated: new Date().toISOString(),
                            user: configStore_1.default.get('user'),
                            id: guid_1.uniqueId(),
                            incidentIdentifier: alertId,
                        };
                        this.setState(function (state) { return ({
                            createBusy: true,
                            // This is passed as a key to NoteInput that re-mounts
                            // (basically so we can reset text input to empty string)
                            noteInputId: guid_1.uniqueId(),
                            activities: tslib_1.__spreadArray([newActivity], tslib_1.__read((state.activities || []))),
                            noteInputText: '',
                        }); });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, incident_1.createIncidentNote(api, orgId, alertId, note)];
                    case 2:
                        newNote_1 = _b.sent();
                        this.setState(function (state) {
                            // Update activities to replace our fake new activity with activity object from server
                            var activities = tslib_1.__spreadArray([
                                newNote_1
                            ], tslib_1.__read(state.activities.filter(function (activity) { return activity !== newActivity; })));
                            return {
                                createBusy: false,
                                activities: activities,
                            };
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.setState(function (state) {
                            var activities = state.activities.filter(function (activity) { return activity !== newActivity; });
                            return {
                                // We clear the textarea immediately when submitting, restore
                                // value when there has been an error
                                noteInputText: note.text,
                                activities: activities,
                                createBusy: false,
                                createError: true,
                                createErrorJSON: error_1.responseJSON || constants_1.DEFAULT_ERROR_JSON,
                            };
                        });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.getIndexAndActivityFromState = function (activity) {
            // `index` should probably be found, if not let error hit Sentry
            var index = _this.state.activities !== null
                ? _this.state.activities.findIndex(function (_a) {
                    var id = _a.id;
                    return id === activity.id;
                })
                : '';
            return [index, _this.state.activities[index]];
        };
        _this.handleDeleteNote = function (activity) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, params, alertId, orgId, _b, index, oldActivity, error_2;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, params = _a.params;
                        alertId = params.alertId, orgId = params.orgId;
                        _b = tslib_1.__read(this.getIndexAndActivityFromState(activity), 2), index = _b[0], oldActivity = _b[1];
                        this.setState(function (state) { return ({
                            activities: removeFromArrayIndex(state.activities, index),
                        }); });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, incident_1.deleteIncidentNote(api, orgId, alertId, activity.id)];
                    case 2:
                        _c.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        error_2 = _c.sent();
                        this.setState(function (state) { return ({
                            activities: replaceAtArrayIndex_1.replaceAtArrayIndex(state.activities, index, oldActivity),
                        }); });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleUpdateNote = function (note, activity) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, params, alertId, orgId, _b, index, oldActivity, error_3;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, params = _a.params;
                        alertId = params.alertId, orgId = params.orgId;
                        _b = tslib_1.__read(this.getIndexAndActivityFromState(activity), 2), index = _b[0], oldActivity = _b[1];
                        this.setState(function (state) { return ({
                            activities: replaceAtArrayIndex_1.replaceAtArrayIndex(state.activities, index, tslib_1.__assign(tslib_1.__assign({}, oldActivity), { comment: note.text })),
                        }); });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, incident_1.updateIncidentNote(api, orgId, alertId, activity.id, note)];
                    case 2:
                        _c.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        error_3 = _c.sent();
                        this.setState(function (state) { return ({
                            activities: replaceAtArrayIndex_1.replaceAtArrayIndex(state.activities, index, oldActivity),
                        }); });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    ActivityContainer.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ActivityContainer.prototype.componentDidUpdate = function (prevProps) {
        // Only refetch if incidentStatus changes.
        //
        // This component can mount before incident details is fully loaded.
        // In which case, `incidentStatus` is null and we will be fetching via `cDM`
        // There's no need to fetch this gets updated due to incident details being loaded
        if (prevProps.incidentStatus !== null &&
            prevProps.incidentStatus !== this.props.incidentStatus) {
            this.fetchData();
        }
    };
    ActivityContainer.prototype.fetchData = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, params, alertId, orgId, activities, err_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, params = _a.params;
                        alertId = params.alertId, orgId = params.orgId;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, incident_1.fetchIncidentActivities(api, orgId, alertId)];
                    case 2:
                        activities = _b.sent();
                        this.setState({ activities: activities, loading: false });
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _b.sent();
                        this.setState({ loading: false, error: !!err_1 });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    ActivityContainer.prototype.render = function () {
        var _a = this.props, api = _a.api, params = _a.params, incident = _a.incident, props = tslib_1.__rest(_a, ["api", "params", "incident"]);
        var alertId = params.alertId;
        var me = configStore_1.default.get('user');
        return (<activity_1.default alertId={alertId} me={me} api={api} {...this.state} loading={this.state.loading || !incident} incident={incident} onCreateNote={this.handleCreateNote} onUpdateNote={this.handleUpdateNote} onDeleteNote={this.handleDeleteNote} {...props}/>);
    };
    return ActivityContainer;
}(react_1.PureComponent));
exports.default = withApi_1.default(ActivityContainer);
function removeFromArrayIndex(array, index) {
    var newArray = tslib_1.__spreadArray([], tslib_1.__read(array));
    newArray.splice(index, 1);
    return newArray;
}
//# sourceMappingURL=index.jsx.map