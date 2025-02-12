# Load the model and encoder during initialization
model = joblib.load('job_relevance_model.pkl')
le = joblib.load('label_encoder.pkl')  # If you saved the encoder
label_encoder=LabelEncoder()
@app.route('/profile')
@login_required
def profile():
    try:
        user_skills = set(current_user.skills.split(','))
        job_field = current_user.job_field_interest.lower()
        disability = current_user.disability

        jobs = Job.query.all()
        job_recommendations = []

        for job in jobs:
            if job.job_field not in label_encoder.classes_:
                label_encoder.fit(list(label_encoder.classes_) + [job.job_field])

            job_field_encoded = label_encoder.transform([job.job_field])[0]
            skills_overlap = len(user_skills & set(job.required_skills.split(',')))
            input_features = [[job_field_encoded, skills_overlap, job.company.rating]]
            
            relevance_score = model.predict_proba(input_features)[0][1]
            job_recommendations.append({
                "job": job,
                "relevance_score": relevance_score,
                "skills_overlap": skills_overlap
            })

        job_recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)

        companies = Company.query.all()
        company_recommendations = [
            {
                "company": company,
                "match_percentage": 100  # Placeholder for match calculation
            } for company in companies
        ]
        company_recommendations.sort(key=lambda x: x['match_percentage'], reverse=True)

        return render_template(
            'profile.html',
            user=current_user,
            job_recommendations=job_recommendations[:5],
            company_recommendations=company_recommendations[:3],
        )
    except Exception as e:
        logger.error(f"Error in profile route: {e}", exc_info=True)
        flash('An error occurred while loading your profile.', 'error')





