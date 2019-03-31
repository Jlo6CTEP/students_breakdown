<template>
    <form v-bind:style="styleSurv">
        <div class="form-group" >
            <label for="courseName">Course name: </label>
            <input type="text" class="form-control" id="courseName" placeholder="ex. Software project">
        </div>

        <div class="form-group" id="numberOfTeamMembers" >
           <label for="minNumberOfTeamMembers"> Minimum number of members in a team: </label>
            <input type="number" class="form-control" id="minNumberOfTeamMembers" placeholder="ex. 2" v-model="minNumb" style = "width: 75px">
            <label for="maxNumberOfTeamMembers"> Maximum number of members in a team: </label>
            <input type="number" class="form-control" id="maxNumberOfTeamMembers" placeholder="ex. 5" v-model="maxNumb" style = "width: 75px">
        </div>
      <!--  <div id="studyGroups" class="form-group">
            <label for="studyGroups">Involve to course project the chosen study groups:</label>
            <br>
            <input type="checkbox" id="BS17-01" value="BS17-01" v-model="checkedGroups">
            <label for="BS17-01">BS17-01</label>
            <input type="checkbox" id="BS17-02" value="BS17-02" v-model="checkedGroups">
            <label for="BS17-01">BS17-02</label>
            <input type="checkbox" id="BS17-03" value="BS17-03" v-model="checkedGroups">
            <label for="BS17-01">BS17-03</label>
            <input type="checkbox" id="BS17-04" value="BS17-04" v-model="checkedGroups">
            <label for="BS17-01">BS17-04</label>
            <input type="checkbox" id="BS17-05" value="BS17-05" v-model="checkedGroups">
            <label for="BS17-01">BS17-05</label>
            <input type="checkbox" id="BS17-06" value="BS17-06" v-model="checkedGroups">
            <label for="BS17-01">BS17-06</label>
            <input type="checkbox" id="BS17-07" value="BS17-07" v-model="checkedGroups">
            <label for="BS17-01">BS17-07</label>
            <input type="checkbox" id="BS17-08" value="BS17-08" v-model="checkedGroups">
            <label for="BS17-01">BS17-08</label>
            <br>
            <span>Chosen groups: {{ checkedGroups }}</span>
        </div>-->
        <div  class="form-group" id="amongGroup">
            <label for="amongGroup"> Form group from students among: </label>
            <br>
            <input type="radio" id="one_among" value="One study group" v-model="picked">
        <label for="one_among">One study group</label>
        <br>
        <input type="radio" id="two_among" value="One TA" v-model="picked">
        <label for="two_among">One TA</label>
        <br>
        <input type="radio" id="three_among" value="One course" v-model="picked">
        <label for="three_among">One course</label>
        <br>
        </div>


        <div class="form-topics" id="projectTopics">
            <label for="projectTopics"> List project topics below </label>
            <br>
            <textarea v-model="projectTopic" placeholder="ex., Topic1, Topic2,..." style = "width: 200px"></textarea>
        </div>
        <div>
            <button v-on:click="createSurvey">Create survey</button>

        </div>
    </form>
</template>

<script>
    export default {
        data() {
            /*
            .form-topics {
                    width: 300px;
                    height: 100px;


                }

                color:red
            }*/
            return {
                cour: 1,
                courseName: 'SWP'
            };
        }
    }

</script>

