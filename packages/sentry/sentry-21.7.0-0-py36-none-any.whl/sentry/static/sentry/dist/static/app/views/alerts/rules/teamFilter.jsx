Object.defineProperty(exports, "__esModule", { value: true });
exports.getTeamParams = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var input_1 = tslib_1.__importDefault(require("app/components/forms/input"));
var locale_1 = require("app/locale");
var filter_1 = tslib_1.__importDefault(require("./filter"));
var ALERT_LIST_QUERY_DEFAULT_TEAMS = ['myteams', 'unassigned'];
function getTeamParams(team) {
    if (team === undefined) {
        return ALERT_LIST_QUERY_DEFAULT_TEAMS;
    }
    if (team === '') {
        return [];
    }
    if (Array.isArray(team)) {
        return team;
    }
    return [team];
}
exports.getTeamParams = getTeamParams;
function TeamFilter(_a) {
    var teams = _a.teams, selectedTeams = _a.selectedTeams, _b = _a.showStatus, showStatus = _b === void 0 ? false : _b, _c = _a.selectedStatus, selectedStatus = _c === void 0 ? new Set() : _c, handleChangeFilter = _a.handleChangeFilter;
    var _d = tslib_1.__read(react_1.useState(), 2), teamFilterSearch = _d[0], setTeamFilterSearch = _d[1];
    var statusOptions = [
        {
            label: locale_1.t('Unresolved'),
            value: 'open',
            checked: selectedStatus.has('open'),
            filtered: false,
        },
        {
            label: locale_1.t('Resolved'),
            value: 'closed',
            checked: selectedStatus.has('closed'),
            filtered: false,
        },
    ];
    var additionalOptions = [
        {
            label: locale_1.t('My Teams'),
            value: 'myteams',
            checked: selectedTeams.has('myteams'),
            filtered: false,
        },
        {
            label: locale_1.t('Unassigned'),
            value: 'unassigned',
            checked: selectedTeams.has('unassigned'),
            filtered: false,
        },
    ];
    var teamItems = teams.map(function (_a) {
        var id = _a.id, name = _a.name;
        return ({
            label: name,
            value: id,
            filtered: teamFilterSearch
                ? !name.toLowerCase().includes(teamFilterSearch.toLowerCase())
                : false,
            checked: selectedTeams.has(id),
        });
    });
    return (<filter_1.default header={<StyledInput autoFocus placeholder={locale_1.t('Filter by team name')} onClick={function (event) {
                event.stopPropagation();
            }} onChange={function (event) {
                setTeamFilterSearch(event.target.value);
            }} value={teamFilterSearch || ''}/>} onFilterChange={handleChangeFilter} dropdownSections={tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read((showStatus
            ? [
                {
                    id: 'status',
                    label: locale_1.t('Status'),
                    items: statusOptions,
                },
            ]
            : []))), [
            {
                id: 'teams',
                label: locale_1.t('Teams'),
                items: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(additionalOptions)), tslib_1.__read(teamItems)),
            },
        ])}/>);
}
exports.default = TeamFilter;
var StyledInput = styled_1.default(input_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  border: none;\n  border-bottom: 1px solid ", ";\n  border-radius: 0;\n"], ["\n  border: none;\n  border-bottom: 1px solid ", ";\n  border-radius: 0;\n"])), function (p) { return p.theme.gray200; });
var templateObject_1;
//# sourceMappingURL=teamFilter.jsx.map